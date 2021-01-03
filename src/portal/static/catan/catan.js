/***********************************\
* Catan Game
\***********************************/
var CatanGame = {
    createNew: function(
        area
    ) {
        var game = {};
        game.board = {};
        game.is_initialized = false;
        game.click_volume = 0.1
        /***********************************\
		 * 加载所有玩家信息
        \***********************************/
        // TODO: read from backend
        // game = catan_load_players(game)
        game.players = []
        game.init_player_action = function(players) {
            game.players = players
            game.player = players[0]
        }

        /***********************************\
		 * 地图设置
         * TODO: remove this part and
         * calculate tile size after
         * fetch tiles data.
        \***********************************/
        game.load_map_config = function(map_name) {
            map = catan_maps[map_name]
            game.board.tiles = map.tiles
            game.board.row = map.row
            game.board.col = map.col
            game.board.robber = map.robber
        }
        game.load_map_config($('#map_name').text());


        /***********************************\
		 * 设置所有的tile
		\***********************************/
        // 计算tile的id到tile的mapping

        game.get_tile_id = function(location) {
            return location.x + location.y * game.board.col;
        };
        game.get_tile = function(location) {
            const id = game.get_tile_id(location);
            return game.board.id_to_tile[id];
        };

        // 回取每个资源格中数字的颜色
        function get_tile_number_color(number){
            if (number>= 6 && number <= 8) {
                return '#dd0000'
            } else {
                return '#333333'
            }
        }


        /***********************************\
		 * 加载地图点线面关系的辅助函数
        \***********************************/
        game = catan_load_utils_for_map(game)

        /************************************************\
        * load function related to build House/Town/Road
        \************************************************/
        catan_load_build(game)

        /***********************************\
		 * 计算所有元素的长宽，自适应屏幕大小
		\***********************************/
        // TODO: set as config.
        var col = game.board.col // first row 8 column, second row 7 column
        var row = game.board.row
        var w = window.innerWidth * 0.98
        var map_w = w * 0.6 * (19 / 24) * (col / row)
        var map_w_ratio = map_w / w
        var left_panel_w = w * (1 - map_w_ratio) / 2
        var right_panel_w = w * (1 - map_w_ratio) / 2
        // 显示中tile的大小
        var tile_w = map_w / col
        var tile_h = tile_w * images.tile.height / images.tile.width
        var map_h = tile_h * 1.0 /4 + tile_h * 3.0 /4 * row
        var panel_h = tile_h * 1.2
        var h = map_h + panel_h + 10
        var card_h = panel_h * 0.7
        var card_w = card_h * images.card.width / images.card.height
        var left_card_x = left_panel_w + map_w * 0.05
        var plus_card_x = left_panel_w + map_w - card_w - map_w * 0.05
        game.sizes = {
            map_col: col,
            map_row: row,
            map_w: map_w,
            map_h: map_h,
            tile_w: tile_w,
            tile_h: tile_h,
            width: w,
            height: h,
            left_panel_w: left_panel_w,
            right_panel_w: right_panel_w,
            panel_h: panel_h,
            card_w: card_w,
            card_h: card_h,
            // 最左的手牌x位置
            left_card_x: left_card_x,
            // 技能卡添加按钮x位置
            plus_card_x: plus_card_x,
        };

        /***********************************\
		 * 设置地图
		\***********************************/
        // 计算某个tile左上角位置
        game.get_tile_tl = function(location) {
            var x = left_panel_w + location.x * tile_w;
            if (location.y % 2 == 1) {
                x += tile_w / 2;
            }
            var y = location.y * tile_h * 3 / 4;
            return {x: x, y: y};
        };
        // 计算某个tile中心位置
        game.get_tile_center = function(location) {
            const tl = game.get_tile_tl(location);
            return {x: tl.x + tile_w/2, y: tl.y + tile_h/2};
        };
        // 加载一个tile，
        // 如果有数字，也加载数字
        // 如果是大陆，也加载大陆架
        game.load_tile = function(tile) {
            const tl = game.get_tile_tl(
                {x: tile.x, y: tile.y}
            );
            const x = tl.x;
            const y = tl.y;

            tile.e = Crafty.e("2D, Canvas, tile_" + tile.type.toLowerCase()).attr({
                x: x,
                y: y,
                z: 1,
                w: tile_w,
                h: tile_h,
            });

            if (tile.number) {
                const text_height = tile_h / 4;
                tile.num_e = Crafty.e("2D, DOM, Text").attr({
                    x: x,
                    y: y + (tile_h - text_height) / 2,
                    z: 11,
                    w: tile_w,
                    h: text_height,
                })
                .text(tile.number)
                .css({ "text-align": "center" })
                .textColor(get_tile_number_color(tile.number))
                .textFont({family: 'Arial', size: `${text_height}px`, weight: 'bold'});

                const center = game.get_tile_center({x: tile.x, y: tile.y})
                const w = tile_h / 4 * 1.5;
                const h = tile_h / 4 * 1.5;
                tile.num_bg_e = Crafty.e(`2D, DOM, number_bg`).attr({
                    x: center.x - w/2,
                    y: center.y - h/2,
                    z: 0,
                    alpha: 0.8,
                    w: w,
                    h: h,
                });
            }

            if (tile.harbor) {
                const center = game.get_tile_center({x: tile.x, y: tile.y})
                const w = tile_h / 4 * 2.5;
                const h = tile_h / 4 * 2.5;
                var touch_area = Crafty.e(`2D, DOM, harbor_${tile.harbor}`).attr({
                    x: center.x - w/2,
                    y: center.y - h/2,
                    z: 0,
                    alpha: 0.8,
                    w: w,
                    h: h,
                });
            }

            // 填充陆地中tile之间的空隙。
            if (tile.type !== 'SEA') {
                Crafty.e("2D, Canvas, tile_land").attr({
                    x: x - tile_w / 100,
                    y: y,
                    z: 0,
                    w: tile_w + tile_w / 30,
                    h: tile_h + tile_h / 50,
                });
            }
        };
        // 加载所有tile和大陆架
        game.load_tiles = function() {
             game.board.tiles.forEach(tile => {
                game.load_tile(tile);
             })
        };
        // 判断tile中是否有陆地
        game.has_land = function(tiles) {
            var is_valid = false;
            tiles.forEach(tile => {
                if (tile.type != 'SEA') {
                    is_valid = true;
                }
            });
            return is_valid;
        };
        // 给定point location，判断是否与陆地相邻
        game.is_land_point = function(location) {
            return game.has_land(
                game.get_adjacent_tiles_from_point(
                    location
                )
            );
        };
        // 给定edge location，判断是否与陆地相邻
        game.is_land_edge = function(location) {
            return game.has_land(
                game.get_adjacent_tiles_from_edge(
                    location
                )
            );
        };
        // 将entity设置为鼠标hover时可见。
        game.set_toggle = function(e) {
            e.alpha = 0;
            e.bind('MouseOver', function(MouseEvent){
                this.alpha = 0.8;
            }).bind('MouseOut', function(MouseEvent){
                this.alpha = 0;
            });
        };

        // 添加point上的点击函数
        game.set_click_point_obj = function(e, w, h) {
            e.bind('Click', function(MouseEvent){
                var point = game.get_point(e.id);
                point.touch_e = e;
                // 是否已有entity。
                if (point.e) {
                    // 已有house，升级成town
                    if (point.name == 'house') {
                        console.log("PLAYER ACTION: try to add a town");
                        data = JSON.stringify({
                            'action': 'BUILD_TOWN',
                            'game_id': $('#gid').text(),
                            'x': point.x,
                            'y': point.y,
                            'z': point.z,
                        });
                        game.socket.send(data);
                    // 已经是town
                    } else {
                        e.unbind('Click');
                    }
                } else {
                    // 未有house和town
                    console.log("PLAYER ACTION: try to add a house");
                    data = JSON.stringify({
                        'action': 'BUILD_HOUSE',
                        'game_id': $('#gid').text(),
                        'x': point.x,
                        'y': point.y,
                        'z': point.z,
                    });
                    game.socket.send(data);
                }
            })
        }

        // 添加edge上的点击函数
        game.set_click_edge_obj = function(e, w, h, z) {
            e.bind('Click', function(MouseEvent){
                var edge = game.get_edge(e.id);
                edge.touch_e = e
                // 是否已有entity。
                if (edge.e) {
                    e.unbind('Click');
                } else {
                    // 未有road
                    console.log("PLAYER ACTION: add a road");
                    data = JSON.stringify({
                        'action': 'BUILD_ROAD',
                        'game_id': $('#gid').text(),
                        'x': edge.x,
                        'y': edge.y,
                        'z': edge.z,
                    });
                    game.socket.send(data);
                }
            })
        }

        // 添加tile上的点击函数
        game.set_click_tile_obj = function(e, tile) {
            e.bind('Click', function(MouseEvent){
                if (game.can_move_robber() == false) {
                    return;
                }
                console.log("PLAYER ACTION: move the robber");
                data = JSON.stringify({
                    'action': 'MOVE_ROBBER',
                    'game_id': $('#gid').text(),
                    'x': tile.x,
                    'y': tile.y,
                });
                game.socket.send(data);
            })
        }
        // 加载所有point位置的touch area
        game.load_point_touch_areas = function() {
            var touch_areas_configs = [
                {'z': -1,},
                {'z': 1,},
            ];
            game.board.tiles.forEach(tile => {
                const tile_center = game.get_tile_center({x: tile.x, y: tile.y})
                touch_areas_configs.forEach((config, index) => {
                    const center = {'x': tile_center.x, 'y': tile_center.y + config.z * tile_h / 2};
                    const w = tile_h / 4;
                    const h = tile_h / 4;
                    if (game.is_land_point({x: tile.x, y: tile.y, z: config.z})) {
                        var touch_area = Crafty.e(`2D, DOM, Mouse, obj_touch_area`).attr({
                            x: center.x - w/2,
                            y: center.y - h/2,
                            center_x: center.x,
                            center_y: center.y,
                            id: game.get_point_id({x: tile.x, y: tile.y, z: config.z}),
                            z: 10,
                            w: w,
                            h: h,
                        }).origin('center');
                        game.set_toggle(touch_area);
                        game.set_click_point_obj(touch_area, w * 1, h * 1);
                    }
                });
            });
        };
        // 加载所有edge位置的touch area
        game.load_edge_touch_areas = function() {
            var touch_areas_configs = [
                {'z': -1,},
                {'z': 0,},
                {'z': 1,},
            ];
            game.board.tiles.forEach(tile => {
                const tile_center = game.get_tile_center({x: tile.x, y: tile.y})
                touch_areas_configs.forEach((config, index) => {
                    const center = {
                        'x': tile_center.x - (config.z == 0 ? tile_w/2 : tile_w/4),
                        'y': tile_center.y + (config.z * tile_h * 3 / 8),
                    };
                    const w = tile_h / 4;
                    const h = tile_h / 4;
                    const rotation = (config.z == 0 ? 90 : 30 * config.z);
                    if (game.is_land_edge({x: tile.x, y: tile.y, z: config.z})) {
                        var touch_area = Crafty.e(`2D, DOM, Mouse, obj_edge_touch_area`).attr({
                            x: center.x - w/2,
                            y: center.y - h/2,
                            center_x: center.x,
                            center_y: center.y,
                            id: game.get_edge_id({x: tile.x, y: tile.y, z: config.z}),
                            z: 10,
                            w: w,
                            h: h,
                        }).origin('center');
                        touch_area.rotation = rotation;
                        game.set_toggle(touch_area);
                        game.set_click_edge_obj(touch_area, w * 2, h * 1, config.z);
                    }
                });
            });
        };
        // 加载所有tile位置的touch area
        game.load_tile_touch_areas = function() {
            game.board.tiles.forEach(tile => {
                const center = game.get_tile_center({x: tile.x, y: tile.y})
                const w = tile_h / 4 * 1.8;
                const h = tile_h / 4 * 1.8;
                if(tile.type != 'SEA') {
                    var touch_area = Crafty.e(`2D, DOM, Mouse, obj_touch_area`).attr({
                        x: center.x - w/2,
                        y: center.y - h/2,
                        center_x: center.x,
                        center_y: center.y,
                        id: game.get_tile_id({x: tile.x, y: tile.y}),
                        z: 10,
                        // alpha: 1,
                        w: w,
                        h: h,
                    }).origin('center');
                    game.set_toggle(touch_area);
                    game.set_click_tile_obj(touch_area, tile);
                }
            });
        };

        /***********************************\
		 * 设置Robber
        \***********************************/
        game.set_robber = function(loc) {
            const robber = game.board.robber;
            // set pixel x, y
            const center = game.get_tile_center(loc)
            robber.e.x = center.x - robber.e.w / 2
            robber.e.y = center.y - robber.e.h / 2

            // set tile effect
            const tile = game.get_tile(loc);
            robber.tile = tile
            tile.robber_e = robber.e;
            if (tile.num_e) {tile.num_e.textColor("#bbbbbb")}
            if (tile.num_bg_e) {tile.num_bg_e.visible = false}
        }
        game.move_robber_action = function(loc) {
            const tile = game.get_tile(loc);
            const pre_tile = game.board.robber.tile;
            if (pre_tile != tile) { // robber 已经在tile上
                if(pre_tile) { // robber 已经在某个tile上，非初始化放置robber
                    pre_tile.robber_e = null;
                    if (pre_tile.num_e) {
                        pre_tile.num_e.textColor(get_tile_number_color(pre_tile.number));
                    }
                    if (pre_tile.num_bg_e) {
                        pre_tile.num_bg_e.visible = true
                    }
                    Crafty.audio.play("punch", 1, game.click_volume)
                }
                game.set_robber(loc)
            }
        }
        game.load_robber = function() {
            const robber = game.board.robber;
            const loc = {x: robber.x, y: robber.y};
            const w = game.sizes.tile_h * 3 / 4
            const h = game.sizes.tile_h * 3 / 4
            robber.e = Crafty.e("2D, DOM, obj_robber").attr({
                z: 10,
                alpha: 1,
                w: w,
                h: h,
            });
            game.set_robber(loc);
        }

        /***********************************\
		 * 加载所有地图区域元素
        \***********************************/
        game.load_map = function() {
            game.load_tiles();
            game.load_tile_touch_areas();
            game.load_point_touch_areas();
            game.load_edge_touch_areas();
            game.load_robber();
        }

        /***********************************\
		 * 加载所有的牌
        \***********************************/
        // game.board.cards = TEST_FULL_CARD_SET;
        game.card_compare = function(a, b) {
            // TODO: add dev cards
            const v = {
                'lumber': 0,
                'brick': 1,
                'wool': 2,
                'grain': 3,
                'ore': 4,
            };
            a_v = v[a.name]
            b_v = v[b.name]
            return a_v - b_v;
        };

        game.get_selected_cards = function () {
            var select_cards = [];
            game.board.cards.forEach(card => {
                if (card.selected) {
                    select_cards.push(card);
                }
            })
            return select_cards;
        };

        game.unselect_card = function (name, count = 1) {
            var count = 1;
            game.board.cards.forEach(card => {
                if (card.selected && card.name == name && count > 0) {
                    card.selected = false;
                    card.e.x = card.e.anchor_x;
                    card.e.y = card.e.anchor_y;
                    count = count - 1;
                }
            })
        };

        game.get_number_of_cards = function () {
            return game.board.cards.length;
        };
        game.can_buy_development_card = function() {
            var has_grain = false;
            var has_wool = false;
            var has_ore = false;
            game.board.cards.forEach(card => {
                if (card.name == 'grain') {
                    has_grain = true;
                } else if (card.name == 'wool') {
                    has_wool = true;
                } else if (card.name == 'ore') {
                    has_ore = true;
                }
            });
            return has_grain && has_wool && has_ore;
        }
        game.unselect_all_cards = function () {
            game.board.cards.forEach(card => {
                if (card.selected) {
                    card.selected = false;
                    card.e.x = card.e.anchor_x;
                    card.e.y = card.e.anchor_y;
                }
            });
        }

        game.get_show_pct = function(max_len, num_cards, card_w, max_pct = 0.8) {
            // show_pct * card_w * num_cards + (1-show_pct) * card_w = max_len
            var show_pct = (max_len - card_w) / ((num_cards - 1) * card_w);
            if (show_pct > max_pct) show_pct = max_pct;
            return show_pct;
        }
        // 计算某个手牌左上角像素
        game.get_card_tl = function(location) {
            const max_len = (plus_card_x - left_card_x) * 0.9;
            const num_cards = game.get_number_of_cards();
            var show_pct = game.get_show_pct(max_len, num_cards, card_w);
            var x = left_card_x + location.x * card_w * show_pct;
            var y = map_h + panel_h * 0.15;
            return {x: x, y: y};
        }
        game.load_cards = function() {
            // var main_panel_w = window.innerWidth * 0.5;
            // var main_panel_h = 100;
            Crafty.e("2D, Canvas, panel").attr({
                x: left_panel_w,
                y: map_h,
                z: 0,
                w: map_w,
                h: panel_h,
            });

            game.board.cards.forEach((card, index) => {
                const tl = game.get_card_tl(
                        {x: index, y: 0}
                );
                const x = tl.x;
                const y = tl.y;
                card.selected = false;
                card.e = Crafty.e("2D, Canvas, Mouse, card_" + card.name).attr({
                    x: x,
                    y: y,
                    anchor_x: x,
                    anchor_y: y,
                    z: 10,
                    w: card_w,
                    h: card_h,
                }).bind('Click', function(MouseEvent){
                    // trading_waiting_mode 不允许选择卡牌
                    if (game.status.trading_waiting_mode) {
                        return;
                    }
                    if(card.selected == false) {
                        console.log('PLAYER ACTION: select ' + card.name);
                        this.y -= 0.15 * card_h;
                        card.selected = true;
                        Crafty.audio.play("click_on", 1, game.click_volume);
                    } else {
                        console.log('PLAYER ACTION: unselect ' + card.name);
                        this.y = y;
                        card.selected = false;
                        Crafty.audio.play("click_off", 1, game.click_volume);
                    }

                    const selected_cards = game.get_selected_cards();
                    if (selected_cards.length > 0) {
                        game.enable_trade_mode();
                        game.set_start_trade_button();
                    } else {
                        game.set_default_button();
                    }
                });
            });
        }

        /***********************************\
		 * 加载所有button相关函数
		\***********************************/
        game = catan_load_buttons(game)

        /***********************************\
		 * 加载所有info相关内容
        \***********************************/
        game = catan_load_info(game)

        /***********************************\
		 * 加载所有state相关内容
        \***********************************/
        game = catan_load_state(game)

        /***********************************\
		 * 开始运行游戏
		\***********************************/
        // 加载主场景
        game.load_main_scene = function() {
            // game.load_map()
            // game.load_cards()
            // game.load_main_button()
            // game.load_info()
            game.socket = CatanWebSocket.createNew(game)
        }

        game.run = function() {
            Crafty.init(w, h, document.getElementById(area));
            // color: #f2d2a9
            Crafty.background('rgb(84,153,202)');
            game = catan_add_loading_scene(
                game,
                left_panel_w + map_w / 4,  // left
                map_h / 3,  // top
                map_w / 2,  // width
                map_h / 16, // info_height
            )
            Crafty.scene("main", game.load_main_scene);
            Crafty.scene("loading", game.load_assets);
            Crafty.scene("loading");
        }

        return game;
    }
};


window.onload = function()
{
    var game = CatanGame.createNew(
        area = "catan_game", // 游戏的显示区域
    );

    game.run();
};
