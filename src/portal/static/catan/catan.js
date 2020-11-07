/***********************************\
* Catan Game
\***********************************/
var CatanGame = {
    createNew: function(
        area,
    ) {
        var game = {};
        game.board = {};
        game.player = {
            name: '小智',
            id: 1,
            sprite: 'player_id_1',
            color: 'blue',
        };
        game.players = [
            game.player,
            {name: '时涛', id: 2, sprite: 'player_id_2', color: 'red',},
            {name: '古今', id: 3, sprite: 'player_id_3', color: 'green',},
        ];

        /***********************************\
		 * 设置所有的tile
		\***********************************/
        game.load_map_config = function(map) {
            game.board.tiles = map.tiles;
            game.board.row = map.row;
            game.board.col = map.col;
            game.board.robber = map.robber;
        }
        // catan_maps.normal
        // catan_maps.fertile_land
        // catan_maps.inland_sea
        game.load_map_config(catan_maps.fertile_land);

        // 计算tile的id到tile的mapping
        game.get_tile_id = function(location) {
            return location.x + location.y * game.board.col;
        };
        game.get_tile = function(location) {
            const id = game.get_tile_id(location);
            return game.board.id_to_tile[id];
        };
        game.board.id_to_tile = {};
        game.board.tiles.forEach(tile => {
            var tid = game.get_tile_id(
                {'x': tile.x, 'y': tile.y}
            );
            game.board.id_to_tile[tid] = tile;
        });

        /***********************************\
		 * 设置所有point上元素
		\***********************************/
        game.board.points = [];
        game.board.id_to_point = {};

        // 计算point的id
        game.get_point_id = function(location) {
            const area = game.board.col * game.board.row;
            const xy_id = location.x + location.y * game.board.col;
            if (location.z == 1) {
                return area + xy_id;
            } else {
                return xy_id;
            }
        }
        game.get_point = function (id) {
            var point = game.board.id_to_point[id];
            if(point) {
                return point;
            } else {
                point = {};
                game.board.points.push(point);
                game.board.id_to_point[id] = point;
                return point;
            }
        }
        /***********************************\
		 * 设置所有edge上元素
		\***********************************/
        game.board.edges = [];
        game.board.id_to_edge = {};

        // 计算edge的id
        game.get_edge_id = function(location) {
            const area = game.board.col * game.board.row;
            const xy_id = location.x + location.y * game.board.col;
            return area * (location.z + 1) + xy_id;
        }
        game.get_edge = function (id) {
            var edge = game.board.id_to_edge[id];
            if(edge) {
                return edge;
            } else {
                edge = {};
                game.board.edges.push(edge);
                game.board.id_to_edge[id] = edge;
                return edge;
            }
        }

        /***********************************\
		 * 设置Robber
		\***********************************/
        game.set_robber = function(location) {
            const center = game.get_tile_center(location);
            const tile = game.get_tile(location);
            const pre_tile = game.board.robber.tile;
            const w = tile_h * 3 / 4;
            const h = tile_h * 3 / 4;
            if (pre_tile == tile) { // robber 已经在tile上
            } else {
                console.log("move the robber");
                if(pre_tile) { // robber 已经在某个tile上
                    pre_tile.robber_e = null;
                    Crafty.audio.stop("punch");
                    Crafty.audio.play("punch", 1, 0.2);
                }
                tile.robber_e = game.board.robber.e;
                game.board.robber.tile = tile;
                game.board.robber.e.x = center.x - w / 2;
                game.board.robber.e.y = center.y - h / 2;
                game.board.robber.e.w = w;
                game.board.robber.e.h = h;

            }
        }
        game.load_robber = function() {
            const robber = game.board.robber;
            const location = {x: robber.x, y: robber.y};
            game.board.robber.e = Crafty.e("2D, Canvas, obj_robber").attr({z: 10, alpha: 1});
            game.set_robber(location);
        }


        /***********************************\
		 * 计算地图中相邻的元素
		\***********************************/
        // 计算与某个点相邻的所有tile。
        game.get_adjacent_tiles_from_point = function (location) {
            var tiles = [];
            var push_tile_by_xy = function(x, y) {
                var loc = {x: x, y: y};
                var tid = game.get_tile_id(loc);
                var tile = game.board.id_to_tile[tid];
                if (tile) {tiles.push(tile);}
            }

            var dx = 1;
            if (location.y % 2 == 0) {dx = -1;}
            push_tile_by_xy(location.x, location.y);
            push_tile_by_xy(location.x, location.y + location.z);
            push_tile_by_xy(location.x + dx, location.y + location.z);
            return tiles;
        }
        // 计算与某条边相邻的所有tile
        game.get_adjacent_tiles_from_edge = function (location) {
            var tiles = [];
            var push_tile_by_xy = function(x, y) {
                var loc = {x: x, y: y};
                var tid = game.get_tile_id(loc);
                var tile = game.board.id_to_tile[tid];
                if (tile) {tiles.push(tile);}
            }
            var dx = -1;
            if (location.z !== 0 && location.y % 2 == 1) {dx = 0;}
            push_tile_by_xy(location.x, location.y);
            push_tile_by_xy(location.x + dx, location.y + location.z);
            return tiles;
        }
        // 计算与某个tile相邻的所有点
        // 计算与某个tile相邻的所有边
        // 计算与某个点相邻的所有边
        // 计算与某个边相邻的所有点

        /***********************************\
		 * 设置所有的手牌
		\***********************************/
        game.board.cards = TEST_FULL_CARD_SET;
        game.card_compare = function(a, b) {
            const v = {
                'lumber': 0,
                'brick': 1,
                'wool': 2,
                'grain': 3,
                'ore': 4,
            };
            // console.log('compare name: ' + a.name);
            // console.log('compare: ' + (v[a.name] - v[b.name]));
            return v[a.name] - v[b.name];
        };
        game.board.cards.sort(game.card_compare);
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

        /***********************************\
		 * 计算所有元素的长宽，自适应屏幕大小
		\***********************************/
        // TODO: set as config.
        var col = game.board.col; // first row 8 column, second row 7 column
        var row = game.board.row;

        var w = window.innerWidth * 0.98;
        var left_panel_w = w * 0.2;
        var right_panel_w = w * 0.2;
        var map_w = w * 0.6;

        // 显示中tile的大小
        var tile_w = map_w / col;
        var tile_h = tile_w * images.tile.height / images.tile.width;

        var map_h = tile_h * 1.0 /4 + tile_h * 3.0 /4 * row;
        var panel_h = tile_h * 1.2;
        var h = map_h + panel_h + 10;

        var card_h = panel_h * 0.7;
        var card_w = card_h * images.card.width / images.card.height;

        var left_card_x = left_panel_w + map_w * 0.05;
        var plus_card_x = left_panel_w + map_w - card_w - map_w * 0.05;

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
		 * 加载所有的图片
		\***********************************/
        game.load_images = function() {
            Crafty.sprite(panel_image_file, {'panel': [0, 0, panel_image_w, panel_image_h]});
            Crafty.sprite(trade_image_file, {'trade': [0, 0, trade_image_w, trade_image_h]});
            Crafty.sprite(single_dice_image_w, single_dice_image_h, dice_image_file,
                {
                    'dice1': [0, 0],
                    'dice2': [1, 0],
                    'dice3': [2, 0],
                }
            );
            for (const [image_type, image_data] of Object.entries(images)) {
                for (const [key, value] of Object.entries(image_data.files)) {
                    var loc = {};
                    loc[image_type + '_' + key] = [0, 0, image_data.width, image_data.height]
                    Crafty.sprite(value, loc);
                }
            }
        };

        /***********************************\
		 * 加载所有的声音
		\***********************************/
        // https://craftyjs.com/api/Crafty-audio.html#Crafty-audio-play
        game.load_sounds = function() {
            var callback = function(){};
            Crafty.load(sounds, callback);
        }

        /***********************************\
		 * 加载地图
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
        // 加载一个tile，如果是大陆，也加载大陆架
        game.load_tile = function(tile) {
            const tl = game.get_tile_tl(
                {x: tile.x, y: tile.y}
            );
            const x = tl.x;
            const y = tl.y;

            tile.e = Crafty.e("2D, Canvas, tile_" + tile.name).attr({
                x: x,
                y: y,
                z: 1,
                w: tile_w,
                h: tile_h,
            });

            // 填充陆地中tile之间的空隙。
            if (tile.name !== 'sea') {
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
                if (tile.name != 'sea') {
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
                // 是否已有entity。
                if (point.e) {
                    // 已有house，升级成town
                    if (point.name == 'house') {
                        console.log("add a town");
                        var house_e = point.e;
                        point.name = 'town';
                        point.e = Crafty.e(`2D, DOM, obj_town`).attr({
                            x: e.center_x - w * 3 / 4,
                            y: e.center_y - h * 3 / 4,
                            z: 5,
                            alpha: 1,
                            w: w * 1.4,
                            h: h * 1.4,
                        });
                        e.unbind('Click');
                        house_e.destroy();
                        Crafty.audio.stop("drilling");
                        Crafty.audio.play("drilling", 1, 0.2);
                    // 已经是town
                    } else {
                        e.unbind('Click');
                    }
                } else {
                    // 未有house和town
                    console.log("add a house");
                    point.name = 'house';
                    point.e = Crafty.e(`2D, DOM, obj_house`).attr({
                        x: e.center_x - w/2,
                        y: e.center_y - h/2,
                        z: 4,
                        alpha: 1,
                        w: w,
                        h: h,
                    });
                    Crafty.audio.stop("hammering");
                    Crafty.audio.play("hammering", 1, 0.2);
                }
            })
        }

        // 添加edge上的点击函数
        game.set_click_edge_obj = function(e, w, h, z) {
            e.bind('Click', function(MouseEvent){
                var edge = game.get_edge(e.id);
                // 是否已有entity。
                if (edge.e) {
                    e.unbind('Click');
                } else {
                    // 未有road
                    console.log("add a road");
                    edge.name = 'house';
                    const rotation = (z == 0 ? 90 : 30 * z);
                    edge.e = Crafty.e(`2D, DOM, obj_road`).attr({
                        x: e.center_x - w/2,
                        y: e.center_y - h/2,
                        z: 3,
                        alpha: 1,
                        w: w,
                        h: h,
                    }).origin('center');
                    edge.e.rotation = rotation;
                    e.unbind('Click');
                    Crafty.audio.stop("hammering");
                    Crafty.audio.play("hammering", 1, 0.2);
                }
            })
        }

        // 添加tile上的点击函数
        game.set_click_tile_obj = function(e, tile) {
            e.bind('Click', function(MouseEvent){
                game.set_robber({x: tile.x, y: tile.y});
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
                const w = tile_h / 4 * 1.5;
                const h = tile_h / 4 * 1.5;
                if(tile.name != 'sea') {
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
        game.load_map = function() {
            game.load_tiles();
            game.load_tile_touch_areas();
            game.load_point_touch_areas();
            game.load_edge_touch_areas();
            game.load_robber();
        }

        /***********************************\
		 * 加载所有button相关函数
		\***********************************/
        game = catan_load_buttons(game);

        /***********************************\
		 * 加载所有的牌
		\***********************************/
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
                        console.log('select ' + card.name);
                        this.y -= 0.15 * card_h;
                        card.selected = true;
                        // Crafty.audio.stop("click_on");
                        // Crafty.audio.stop("click_off");
                        Crafty.audio.play("click_on");
                    } else {
                        console.log('unselect ' + card.name);
                        this.y = y;
                        card.selected = false;
                        // Crafty.audio.stop("click_on");
                        // Crafty.audio.stop("click_off");
                        Crafty.audio.play("click_off", 1, 0.5);
                    }

                    const selected_cards = game.get_selected_cards();
                    if (selected_cards.length > 0) {
                        console.log("select at lease 1 card");
                        game.enable_trade_mode();
                        game.set_start_trade_button();
                    } else {
                        game.set_default_button();
                    }
                });
            });
        }

        /***********************************\
		 * 开始运行游戏
		\***********************************/
        game.run = function() {
            Crafty.init(w, h, document.getElementById(area));
            // #f2d2a9
            Crafty.background('rgb(84,153,202)');

            game.load_images();
            game.load_sounds();
            game.load_map();
            game.load_cards();
            game.load_main_button();
            // game.start();
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
