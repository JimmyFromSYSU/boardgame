
/***********************************\
* Minesweeper assets
\***********************************/
var assets = {
    "sprites": {
        "/static/images/classic/minesweeper/cover.jpeg": {
            "tile": 225,
            "tileh": 225,
            "map": { "cover": [0,0]},
        },
        "/static/images/classic/minesweeper/cover_2.jpeg": {
            "tile": 225,
            "tileh": 225,
            "map": { "cover_2": [0,0]},
        },
        "/static/images/classic/minesweeper/land.jpeg": {
            "tile": 225,
            "tileh": 225,
            "map": { "land": [0,0]},
        },
        "/static/images/classic/minesweeper/land_2.jpeg": {
            "tile": 225,
            "tileh": 225,
            "map": { "land_2": [0,0]},
        },
        "/static/images/classic/minesweeper/mine.jpeg": {
            "tile": 225,
            "tileh": 225,
            "map": { "mine": [0,0]},
        },
        "/static/images/classic/minesweeper/flag.png": {
            "tile": 225,
            "tileh": 225,
            "map": { "flag": [0,0]},
        },
    },
    "audio": {
        "button_click_on": ["/static/sounds/classic/minesweeper/button_click_on.wav"],
        "button_click_off": ["/static/sounds/classic/minesweeper/button_click_off.wav"],
        "ding": ["/static/sounds/classic/minesweeper/ding.wav"],
    },
}

const neighbor = [
    {dr: -1, dc: -1},
    {dr: -1, dc: 0},
    {dr: -1, dc: 1},
    {dr: 0, dc: -1},
    // {dr: 0, dc: 0},
    {dr: 0, dc: 1},
    {dr: 1, dc: -1},
    {dr: 1, dc: 0},
    {dr: 1, dc: 1},
]

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

/***********************************\
* Minesweeper Game
\***********************************/
var MinesweeperGame = {
    createNew: function(
        area
    ) {
        var game = {}
        game.board = {}

        game.bg_color = 'rgb(249,214,179)'
        // screen.orientation.lock('portrait').catch(function(error) {
        // });
        game.release = function () {
            console.log("game.release")
            if (game.grids && game.col && game.row) {
                for (var r = 0; r < game.row; r = r + 1) {
                    for (var c = 0; c < game.col; c = c + 1) {
                        var tile = game.grids[r][c]
                        if (tile.cover_e) {
                            tile.cover_e.destroy()
                        } else if (tile.number_e) {
                            tile.number_e.destroy()
                        } else if (tile.land_e) {
                            tile.land_e.destroy()
                        }
                    }
                }
            }
        }

        game.setup_config = function() {
            game.click_volume = 0.3

            game.screen_w = window.innerWidth
            game.screen_h = window.innerHeight
            game.padding_left = game.screen_w * 0.05
            game.padding_right = game.padding_left
            game.padding_top = 100
            game.padding_bottom = 100

            game.total_mine = 0
            game.hit_mine = 0
            game.max_hit_mine = 3
            game.pct_of_mine = 0.1 + (Math.random() / 10)
            console.log(`game.pct_of_mine = ${Math.random()}`)
            // game.col = 50
            // game.tile_len =  Math.floor((game.screen_w - game.padding_left - game.padding_right) / game.col)
            // game.row = Math.floor((game.screen_h - game.padding_top - game.padding_bottom) / game.tile_len)
            game.tile_len = 30
            game.col = Math.floor((game.screen_w - game.padding_left - game.padding_right) / game.tile_len)
            game.row = Math.floor((game.screen_h - game.padding_top - game.padding_bottom) / game.tile_len)

            game.z_level = {
                flag: 15,
                cover: 10,
                number: 5,
                land: 0,
            }
        }

        game.get_tile_left_top = function(row, col) {
            return {
                x: game.padding_left + game.tile_len * col,
                y: game.padding_top + game.tile_len * row
            }
        }

        game.show_all_mine = async function() {
            var tiles = []
            for (var r = 0; r < game.row; r = r + 1) {
                for (var c = 0; c < game.col; c = c + 1) {
                    tile = game.grids[r][c]
                    if(tile.is_mine && tile.is_cover) {
                        tiles.push(tile)
                    }
                }
            }

            shuffleArray(tiles)

            for (var i = 0; i < tiles.length; i = i + 1) {
                game.show_tile(tiles[i])
                await sleep(1)
            }
        }

        game.show_number = function(tile) {
            if(tile.number_e) {
                tile.number_e.alpha = 1
            }
        }

        game.in_grids = function(r, c) {
            if(r >=0 && r < game.row && c >= 0 && c < game.col) {
                return true
            } else {
                return false
            }
        }

        game.get_number_color = function (number) {
            if (number == 1) return '#0000ff'
            else if (number == 2) return '#008888'
            else if (number == 3) return '#ff0000'
            else if (number == 4) return '#000088'
            else if (number == 5) return '#008800'
            else if (number == 6) return '#880000'
            else if (number == 7) return '#004444'
            else if (number == 8) return '#000000'
        }

        game.precomp_tile = function(tile, r, c) {
            if(tile.is_mine) {
                tile.number = 9
            } else {
                var number = 0
                for (var i = 0; i < neighbor.length; i = i + 1) {
                    const new_r = r + neighbor[i].dr
                    const new_c = c + neighbor[i].dc
                    if (game.in_grids(new_r, new_c) && game.grids[new_r][new_c].is_mine) {
                        number = number + 1
                    }
                }
                tile.number = number
                if (tile.number > 0 && tile.number < 9) {
                    const left_top = game.get_tile_left_top(r, c)
                    const text_padding_left = game.tile_len / 3
                    const text_padding_top = game.tile_len / 6
                    const font_size = game.tile_len * 2 / 3
                    tile.number_e = Crafty.e(`2D, DOM, Text`).attr({
                        x: left_top.x + text_padding_left,
                        y: left_top.y + text_padding_top,
                        z: game.z_level.number,
                        w: game.tile_len,
                        h: game.tile_len,
                        alpha: 0,
                    }).text(tile.number.toString())
                    .textColor(game.get_number_color(tile.number))
                    .textFont({family: 'Arial', size: `${font_size}px`, weight: 'bold'});
                }
            }
        }

        game.precomp_tiles = function() {
            for (var r = 0; r < game.row; r = r + 1) {
                for (var c = 0; c < game.col; c = c + 1) {
                    tile = game.grids[r][c]
                    game.precomp_tile(tile, r, c)
                }
            }
        }

        // show one tile
        game.show_tile = function(tile) {
            tile.cover_e.alpha = 0
            tile.land_e.alpha = 1
            tile.cover_e.unbind('MouseOut').unbind('MouseOver').unbind('Click').unbind('MouseUp')
            tile.is_cover = false
            game.remove_flag(tile, silent=true)
            game.show_number(tile)
        }

        game.get_neighbor_tiles = function(tile) {
            var tiles = []
            for (var i = 0; i < neighbor.length; i = i + 1) {
                const new_r = tile.r + neighbor[i].dr
                const new_c = tile.c + neighbor[i].dc
                if (game.in_grids(new_r, new_c)) {
                    tiles.push(game.grids[new_r][new_c])
                }
            }
            return tiles
        }

        game.bfs_show_tile = async function(first_tile) {
            var queue = [first_tile]
            game.show_tile(first_tile)

            while(queue.length > 0) {
                var tile = queue.shift()
                // console.log(queue)
                if(tile.number == 0) {
                    tiles = game.get_neighbor_tiles(tile)
                    // console.log(tiles)
                    for (var i = 0; i < tiles.length; i = i + 1) {
                        if(tiles[i].is_cover) {
                            // console.log(tiles[i])
                            game.show_tile(tiles[i])
                            queue.push(tiles[i])
                        }
                    }
                    // await sleep(1);
                }
            }
        }

        game.set_click_cover = function(e, tile) {
            e.bind('Click', function(MouseEvent){
                // remove flag first
                if (tile.is_flag) {
                    game.remove_flag(tile)
                    tile.is_flag = false
                } else {
                    if (tile.is_mine) {
                        game.hit_mine = game.hit_mine + 1
                        Crafty.audio.play("ding", 1, game.click_volume);
                        if (game.hit_mine >= game.max_hit_mine) {
                            game.show_tile(tile)
                            game.show_all_mine()
                        } else {
                            game.show_tile(tile)
                        }
                    } else {
                        Crafty.audio.play("button_click_on", 1, game.click_volume);
                        // game.show_tile(tile)
                        game.bfs_show_tile(tile)
                    }
                }
            })
        }

        game.set_click_flag = function(e, tile) {
            e.bind('MouseUp', function(e) {
                if( e.mouseButton == Crafty.mouseButtons.RIGHT ) {
                    if (tile.is_cover) {
                        if(tile.is_flag) {
                            game.remove_flag(tile)
                            tile.is_flag = false
                        } else {
                            game.show_flag(tile)
                            tile.is_flag = true
                        }
                    }
                }
            })
        }

        game.show_flag = function(tile, silent=false) {
            if (tile.flag_e) {
                tile.flag_e.alpha = 1
            } else {
                const left_top = game.get_tile_left_top(tile.r, tile.c)
                tile.flag_e = Crafty.e(`2D, DOM, flag`).attr({
                    x: left_top.x,
                    y: left_top.y,
                    z: game.z_level.flag,
                    w: game.tile_len,
                    h: game.tile_len,
                    alpha: 1,
                })
            }
            if (! silent)
                Crafty.audio.play("button_click_on", 1, game.click_volume);
        }

        game.remove_flag = function(tile, silent=false) {
            if(tile.flag_e) {
                tile.flag_e.alpha = 0
            }
            if (! silent)
                Crafty.audio.play("button_click_off", 1, game.click_volume);
        }

        game.init_map = function() {
            game.grids = []

            gen_random_mine = function() {
                // const r = Math.floor(Math.random() * 6)
                if (Math.random() < game.pct_of_mine) {
                    return true
                } else {
                    return false
                }
            }

            gen_tile_cover_img = function(r, c) {
                if ( (r + c) % 2 == 0) {
                    return "cover"
                } else {
                    return "cover_2"
                }
            }

            gen_tile_land_img = function(r, c, is_mine) {
                if (is_mine) {
                    return "mine"
                }
                else if ( (r + c) % 2 == 0) {
                    return "land"
                } else {
                    return "land_2"
                }
            }

            set_hightligt = function(e) {
                const alpha = e.alpha
                e.bind('MouseOver', function(MouseEvent){
                    this.alpha = 0.4;
                }).bind('MouseOut', function(MouseEvent){
                    this.alpha = alpha;
                });
            };

            for (var r = 0; r < game.row; r = r + 1) {
                row_grids = []
                for (var c = 0; c < game.col; c = c + 1) {
                    const left_top = game.get_tile_left_top(r, c)
                    const is_mine = gen_random_mine()
                    var cover_e = Crafty.e(`2D, DOM, Mouse, ${gen_tile_cover_img(r, c)}`).attr({
                        x: left_top.x,
                        y: left_top.y,
                        z: game.z_level.cover,
                        w: game.tile_len,
                        h: game.tile_len,
                    })
                    set_hightligt(cover_e)

                    var land_e = Crafty.e(`2D, DOM, Mouse, ${gen_tile_land_img(r, c, is_mine)}`).attr({
                        x: left_top.x,
                        y: left_top.y,
                        z: game.z_level.land,
                        w: game.tile_len,
                        h: game.tile_len,
                        alpha: 0,
                    })


                    tile = {
                        'r': r,
                        'c': c,
                        'cover_e': cover_e,
                        'land_e': land_e,
                        'is_mine': is_mine,
                        'is_cover': true,
                        'is_flag': false,
                    }
                    if (is_mine) {game.total_mine = game.total_mine + 1}
                    game.set_click_cover(cover_e, tile)
                    game.set_click_flag(cover_e, tile)
                    row_grids.push(tile)
                }
                game.grids.push(row_grids)
            }
            console.log(`total mine: ${game.total_mine}`)
        }

        game.load_main_scene = function() {
            console.log("game.load_main_scene")

            var loaded = function() {
            }
            var progress = function(e) {
            };
            var error_loading = function(e) {
            };
            // catch audio error
            try {
                Crafty.load(assets, loaded, progress, error_loading);
            } catch (error) {
                console.error(error);
            }

            game.release()
            game.setup_config()
            game.init_map()
            game.precomp_tiles()
        }

        game.run = function() {
            Crafty.init(game.screen_w, game.screen_h, document.getElementById(area));
            Crafty.background(game.bg_color);

            Crafty.scene("main", game.load_main_scene);
            // Crafty.scene("loading", game.load_assets);
            Crafty.scene("main");
        }

        return game;
    }
};

window.onload = function()
{
    var game = MinesweeperGame.createNew(
        area = "minesweeper_game", // 游戏的显示区域
    );

    game.run();
};
