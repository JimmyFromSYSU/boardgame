
/***********************************\
* Minesweeper Game
\***********************************/
var MinesweeperGame = {
    createNew: function(
        area
    ) {
        var game = {}
        game.board = {}

        game.bg_color = 'rgb(84,153,202)'
        // screen.orientation.lock("portrait")
        // screen.orientation.lock("landscape")
        screen.orientation.lock('portrait').catch(function(error) {
            // game.bg_color = 'rgb(255,0,255)'
            // Crafty.background(game.bg_color)
            // // whatever
            // console.log(game.bg_color)
            // alert(`${error}`)
        });

        var w = window.innerWidth
        var h = window.innerHeight
        // alert(`${w} * ${h}`)
        game.load_main_scene = function() {
            console.log("load_main_scene")
        }

        game.run = function() {
            Crafty.init(w, h, document.getElementById(area));
            // color: #f2d2a9
            console.log(game.bg_color)
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
