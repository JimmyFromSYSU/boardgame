/***********************************\
 * 设置Dice
\***********************************/
var catan_load_dice = function(game) {
    game.roll_dice = function(e, number) {
        if (number == null || number == undefined) {
            number = Math.floor(Math.random() * 6);
        }
        var animation = [0, 1, 2, 3, 4, 5];
        animation = animation.concat(animation);
        animation.sort(() => Math.random() - 0.5);
        animation.push(number);

        var animation_list = animation.map(v => [v, 0]);
        var reel = e.getReel('roll_dice');
        if (reel) {
            reel.frames = animation_list;
        } else {
            e.reel('roll_dice', 1500, animation_list);
        }
        e.animate('roll_dice', 1);
        Crafty.audio.play("roll_dice", 1, game.click_volume);
        return number + 1;
    }
    game.roll_dice_action = function(num1, num2) {
        game.roll_dice(game.dice1, num1);
        game.roll_dice(game.dice2, num2);
    }
    game.send_roll_dice_request = function() {
        if (game.dice1.isPlaying() || game.dice2.isPlaying()) {
            return null;
        }
        const num1 = Math.floor(Math.random() * 6)
        const num2 = Math.floor(Math.random() * 6)
        console.log(`PLAYER ACTION: try to roll dice ${num1 + 1} + ${num2 + 1}`)
        data = JSON.stringify({
            'action': 'ROLL_DICE',
            'num1': num1,
            'num2': num2,
        });
        game.socket.send(data)
    }
    game.load_dices = function() {
        const dice_left = game.sizes.left_panel_w / 3;
        // const dice_top = map_h + text_height;
        const dice_top = game.sizes.map_h + game.sizes.panel_h * 0.05;
        // const dice_w = game.sizes.left_panel_w / 3;
        const dice_h = game.sizes.panel_h * 0.9; // height - text_height;
        const dice_w = dice_h;

        // Dice button
        game.dice1 = Crafty.e("2D, Canvas, Mouse, SpriteAnimation, dice1").attr({
            x: dice_left,
            y: dice_top,
            z: 0,
            name: 'dice',
            w: dice_w,
            h: dice_h,
        }).bind('MouseUp', function(MouseEvent){
            game.send_roll_dice_request()
        })

        // 骰子
        game.dice2 = Crafty.e("2D, Canvas, Mouse, SpriteAnimation, dice2").attr({
            x: dice_left + dice_w,
            y: dice_top,
            z: 0,
            name: 'dice',
            w: dice_w,
            h: dice_h,
        }).bind('MouseUp', function(MouseEvent){
            game.send_roll_dice_request()
        })
    }

    return game
}
