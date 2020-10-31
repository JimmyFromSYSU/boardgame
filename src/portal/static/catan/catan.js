/***********************************\
* Catan Game
\***********************************/
var CatanGame = {
    createNew: function(
        area,
    ) {
        var game = {};
        game.board = {}

        // 加载地图数据
        // game.board.tiles = catan_maps.normal.tiles;
        game.board.row = catan_maps.fertile_land.row;
        game.board.col = catan_maps.fertile_land.col;
        game.board.tiles = catan_maps.fertile_land.tiles;

        // 计算tile的id到tile的mapping
        game.get_tile_id = function(location) {
            return location.x + location.y * game.board.col;
        };
        game.board.id_to_tile = {}
        game.board.tiles.forEach(tile => {
            var tid = game.get_tile_id(
                {'x': tile.x, 'y': tile.y}
            );
            // console.log(tid);
            game.board.id_to_tile[tid] = tile;
        });

        /***********************************\
		 * 计算地图中相邻的元素
		\***********************************/
        // 计算与某个点相邻的所有tile。
        game.get_adjacent_tiles_from_point = function (location) {
            var tiles = [];
            var push_tile_by_xy = function(x, y) {
                var loc = {x: x, y: y};
                // console.log(loc);
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
                // console.log(loc);
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
        game.board.cards = [
            {'name': 'lumber'},
            {'name': 'lumber'},
            {'name': 'lumber'},
            {'name': 'lumber'},
            {'name': 'brick'},
            {'name': 'brick'},
            {'name': 'brick'},
            {'name': 'brick'},
            {'name': 'wool'},
            {'name': 'wool'},
            {'name': 'wool'},
            {'name': 'wool'},
            {'name': 'grain'},
            {'name': 'grain'},
            {'name': 'grain'},
            {'name': 'grain'},
            {'name': 'ore'},
            {'name': 'ore'},
            {'name': 'ore'},
            {'name': 'ore'},
        ];

        /***********************************\
		 * 图片文件与大小设置
		\***********************************/
        var tile_image_files = {
            'brick': '/static/images/catan/map/brick.png',
            'wool': '/static/images/catan/map/wool.png',
            'ore': '/static/images/catan/map/ore.png',
            'lumber': '/static/images/catan/map/lumber.png',
            'grain': '/static/images/catan/map/grain.png',
            'desert': '/static/images/catan/map/desert.png',
            'sea': '/static/images/catan/map/sea.png',
            'land': '/static/images/catan/map/land.png',
        };
        // tile图片的大小
        var tile_image_w = 500;
        var tile_image_h = 575;
        var touch_area_image_file = '/static/images/catan/map/touch_area.png';
        var touch_area_image_w = 120;
        var touch_area_image_h = 120;
        var panel_image_file = "/static/images/catan/panel/panel.png";
        var panel_image_w = 512;
        var panel_image_h = 240;

        var card_image_files = {
            'brick': '/static/images/catan/card/brick.png',
            'wool': '/static/images/catan/card/wool.png',
            'ore': '/static/images/catan/card/ore.png',
            'lumber': '/static/images/catan/card/lumber.png',
            'grain': '/static/images/catan/card/grain.png',
        }
        var card_image_w = 284;
        var card_image_h = 429;

        /***********************************\
		 * 计算所有元素的长宽，自适应屏幕大小
		\***********************************/
        // TODO: set as config.
        var col = game.board.col; // first row 8 column, second row 7 column
        var row = game.board.row;

        // console.log("screen.width: " + screen.width);
        // console.log("window.innerWidth: " + window.innerWidth);
        var w = window.innerWidth * 0.98;
        var left_panel_w = w * 0.2;
        var right_panel_w = w * 0.2;
        var map_w = w * 0.6;

        // 显示中tile的大小
        var tile_w = map_w / col;
        var tile_h = tile_w * tile_image_h / tile_image_w;

        var map_h = tile_h * 1.0 /4 + tile_h * 3.0 /4 * row;
        var bottom_panel_h = tile_h * 1.2;
        var h = map_h + bottom_panel_h;

        var card_h = bottom_panel_h * 0.8;
        var card_w = card_h * card_image_w / card_image_h;

        /***********************************\
		 * 加载所有的图片
		\***********************************/
        game.load_images = function() {
            Crafty.sprite(panel_image_file, {'panel': [0, 0, panel_image_w, panel_image_h]});
            Crafty.sprite(touch_area_image_file, {'touch_area': [0, 0, touch_area_image_w, touch_area_image_h]});

            for (const [key, value] of Object.entries(tile_image_files)) {
                // console.log(`${key}: ${value}`);
                var loc = {};
                loc[key] = [0, 0, tile_image_w, tile_image_h]
                Crafty.sprite(value, loc);
            }

            for (const [key, value] of Object.entries(card_image_files)) {
                // console.log(`${key}: ${value}`);
                var loc = {};
                loc[key + '_card'] = [0, 0, card_image_w, card_image_h]
                Crafty.sprite(value, loc);
            }
        }

        /***********************************\
		 * 加载地图
		\***********************************/
        // 计算某个tile所在的左上角像素
        game.get_tile_xy = function(location) {
            var x = left_panel_w + location.x * tile_w;
            if (location.y % 2 == 1) {
                x += tile_w / 2;
            }
            var y = location.y * tile_h * 3 / 4;
            return [x, y];
        }
        game.load_map = function() {
            game.board.tiles.forEach(tile => {
                const [x, y] = game.get_tile_xy(
                    {x: tile.x, y: tile.y}
                );

                Crafty.e("2D, Canvas, " + tile.name).attr({
                    x: x,
                    y: y,
                    z: 1,
                    w: tile_w,
                    h: tile_h,
                });

                // 鼠标点击位
                const r = tile_h / 8;
                // 区块中心的点击区域更大
                const tile_r = r * 2;
                var click_areas_configs = [
                    {'type': 'tile',  x: x + tile_w / 2 - tile_r, y: y + tile_h / 2     - tile_r},
                    {'type': 'point', x: x + tile_w / 2 - r, y: y                  - r, loc_z: -1},
                    {'type': 'point', x: x + tile_w / 2 - r, y: y + tile_h         - r, loc_z: 1},
                    {'type': 'edge',  x: x + tile_w / 4 - r, y: y + tile_h / 8     - r, loc_z: -1},
                    {'type': 'edge',  x: x + tile_w / 4 - r, y: y + tile_h * 7 / 8 - r, loc_z: 1},
                    {'type': 'edge',  x: x - r,              y: y + tile_h / 2     - r, loc_z: 0},
                ]

                click_areas_configs.forEach((config, index) => {
                    const transparency = 0.0;
                    var d = 2 * r;
                    if (config.type === 'tile') {d = 2 * tile_r;}
                    // var color = `rgba(255,255,255,${transparency})`;
                    Crafty.e("2D, Canvas, Mouse, touch_area").attr({
                        x: config.x,
                        y: config.y,
                        z: 2,
                        alpha: transparency,
                        w: d,
                        h: d,
                        radius: r,
                        type: config.type,
                    }).bind('Click', function(MouseEvent){
                        if (config.type === 'tile') {
                            if (tile.name !== 'sea') {
                                this.alpha = 1;
                                console.log("select " + config.type + ": " + tile.x + " " +tile.y);
                            }
                        } else {
                            var tiles = [];
                            if(config.type === 'point') {
                                tiles = game.get_adjacent_tiles_from_point(
                                    {'x': tile.x, 'y': tile.y, 'z': config.loc_z}
                                );
                            } else if (config.type === 'edge') {
                                tiles = game.get_adjacent_tiles_from_edge(
                                    {'x': tile.x, 'y': tile.y, 'z': config.loc_z}
                                );
                            }

                            var is_valid = false;
                            tiles.forEach(tile => {
                                if (tile.name != 'sea') {
                                    is_valid = true;
                                }
                            });
                            if (is_valid) {
                                this.alpha = 1;
                                console.log("select " + config.type + ": " + tile.x + " " + tile.y + " " + config.loc_z);
                            }
                        }
                    });
                });

                // 填充陆地中tile之间的空隙。
                if (tile.name !== 'sea') {
                    // console.log(tile.name);
                    Crafty.e("2D, Canvas, land").attr({
                        x: x - tile_w / 100,
                        y: y,
                        z: 0,
                        w: tile_w + tile_w / 30,
                        h: tile_h + tile_h / 50,
                    });
                }
            });
        }

        /***********************************\
		 * 加载所有的牌
		\***********************************/
        // 计算某个手牌所在的左上角像素
        game.get_card_xy = function(location) {
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
                const [x, y] = game.get_card_xy(
                        {x: index, y: 0}
                );
                const card_name = card.name + "_card";
                card.e = Crafty.e("2D, Canvas, Mouse, " + card_name).attr({
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


        /***********************************\
		 * 开始运行游戏
		\***********************************/
        game.run = function() {
            Crafty.init(w, h, document.getElementById(area));
            // #f2d2a9
            Crafty.background('rgb(84,153,202)');

            game.load_images();
            game.load_map();
            game.load_cards()
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
