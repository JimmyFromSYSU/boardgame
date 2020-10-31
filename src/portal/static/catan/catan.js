/***********************************\
* Catan Game
\***********************************/
var CatanGame = {
    createNew: function(
        area,
    ) {
        var game = {};
        game.board = {};

        /***********************************\
		 * 设置所有的tile
		\***********************************/
        // game.board.tiles = catan_maps.normal.tiles;
        game.board.tiles = catan_maps.fertile_land.tiles;
        game.board.row = catan_maps.fertile_land.row;
        game.board.col = catan_maps.fertile_land.col;
        // 计算tile的id到tile的mapping
        game.get_tile_id = function(location) {
            return location.x + location.y * game.board.col;
        };
        game.board.id_to_tile = {}
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
        var bottom_panel_h = tile_h * 1.2;
        var h = map_h + bottom_panel_h;

        var card_h = bottom_panel_h * 0.8;
        var card_w = card_h * images.card.width / images.card.height;


        /***********************************\
		 * 加载所有的图片
		\***********************************/
        game.load_images = function() {
            Crafty.sprite(panel_image_file, {'panel': [0, 0, panel_image_w, panel_image_h]});

            for (const [image_type, image_data] of Object.entries(images)) {
                for (const [key, value] of Object.entries(image_data.files)) {
                    var loc = {};
                    loc[image_type + '_' + key] = [0, 0, image_data.width, image_data.height]
                    Crafty.sprite(value, loc);
                }
            }
        };

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
            return [x, y];
        };
        // 计算某个tile中心位置
        game.get_tile_center = function(location) {
            const [x, y] = game.get_tile_tl(location);
            return [x + tile_w/2, y + tile_h/2];
        };
        // 加载一个tile，如果是大陆，也加载大陆架
        game.load_tile = function(tile) {
            const [x, y] = game.get_tile_tl(
                {x: tile.x, y: tile.y}
            );

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
                this.alpha = 0.5;
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
                        point.e.destroy();
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
                }
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
                    const center = {'x': tile_center[0], 'y': tile_center[1] + config.z * tile_h / 2};
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
                            // alpha: 1,
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
                        'x': tile_center[0] - (config.z == 0 ? tile_w/2 : tile_w/4),
                        'y': tile_center[1] + (config.z * tile_h * 3 / 8),
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
                            // alpha: 1,
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
                const tile_center = game.get_tile_center({x: tile.x, y: tile.y})
                const center = {'x': tile_center[0], 'y': tile_center[1]};
                const w = tile_h / 4 * 1.5;
                const h = tile_h / 4 * 1.5;
                if(tile.name != 'sea') {
                    var touch_area = Crafty.e(`2D, DOM, Mouse, obj_touch_area`).attr({
                        x: center.x - w/2,
                        y: center.y - h/2,
                        center_x: center.x,
                        center_y: center.y,
                        z: 10,
                        // alpha: 1,
                        w: w,
                        h: h,
                    }).origin('center');
                    game.set_toggle(touch_area);
                }
            });
        };
        game.load_map = function() {
            game.load_tiles();
            game.load_tile_touch_areas();
            game.load_point_touch_areas();
            game.load_edge_touch_areas();
        }

        /***********************************\
		 * 加载所有的牌
		\***********************************/
        // 计算某个手牌左上角像素
        game.get_card_tl = function(location) {
            var x = left_panel_w + map_w * 0.03 + location.x * card_w * 0.5;
            var y = map_h + bottom_panel_h * 0.15;
            return [x, y];
        }
        game.load_cards = function() {
            var main_panel_w = window.innerWidth * 0.5;
            var main_panel_h = 100;
            // two panel in bottom
            Crafty.e("2D, Canvas, panel").attr({
                x: left_panel_w,
                y: map_h,
                z: 0,
                w: map_w,
                h: bottom_panel_h,
            });

            game.board.cards.forEach((card, index) => {
                const [x, y] = game.get_card_tl(
                        {x: index, y: 0}
                );
                card.e = Crafty.e("2D, Canvas, Mouse, card_" + card.name).attr({
                    x: x,
                    y: y,
                    z: 10,
                    w: card_w,
                    h: card_h,
                    selected: false,
                }).bind('Click', function(MouseEvent){
                    if(this.y == y) {
                        console.log('select ' + card.name);
                        this.y -= 0.15 * card_h;
                        this.selected = true;
                    } else {
                        this.y = y;
                        this.selected = false;
                    }
                });
            });
        }

        game.load_main_button = function() {
        }

        /***********************************\
		 * 开始运行游戏
		\***********************************/
        game.run = function() {
            Crafty.init(w, h, document.getElementById(area));
            // #f2d2a9
            Crafty.background('rgb(84,153,202)');

            game.load_images();
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
