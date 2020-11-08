var catan_load_buttons = function(game) {
    game.status = {
        trading_mode: false,
        trading_waiting_mode: false,
    };
    game.control = {
        main_text: {},
        yes_btn: {},
        no_btn: {},
        plus_btn: {},

        select_player_panel: {},
        select_player_text: {},


        select_card_text: {},
        select_card_panel: {},

        buy_cards_panel: {},
        trade_buy_cards: [],

        pay_cards_panel: {},
        trade_pay_cards: [],

        trade_mark: {},
    };
    const click_volume = 0.5;
    const click_button = function(e) {
        e.x = e.anchor_x + 5;
        e.y = e.anchor_y + 5;
    }
    const reset_button = function(e) {
        e.x = e.anchor_x;
        e.y = e.anchor_y;
    }

    /***********************************\
     * Main button 相关函数
    \***********************************/
    // 设置按钮按下时的位移动画
    game.set_button_movement = function(e, callback, sound = "click_on", bind_e) {
        if ( (!e.anchor_x) || (!e.anchor_y)) {
            console.warn(`must set anchor_x/anchor_y for ${e}`);
            return;
        }
        e.unbind('MouseDown').unbind('MouseUp');
        e.bind('MouseDown', function(MouseEvent){
            click_button(this);
            if (bind_e) {click_button(bind_e)}
        }).bind('MouseUp', function(MouseEvent){
            reset_button(this);
            if (bind_e) {reset_button(bind_e)}
            Crafty.audio.play(sound, 1, click_volume);
            if (callback) {
                callback()
            }
        }).bind('MouseOut', function(MouseEvent){
            reset_button(this);
            if (bind_e) {reset_button(bind_e)}
        });
    }
    // 隐藏并取消按钮功能
    game.disable_button = function(btn) {
        if (btn.bg_e) {
            btn.bg_e.alpha = 0;
        }
        btn.e.alpha = 0;
        btn.e.unbind('MouseDown').unbind('MouseUp').unbind('MouseOut').unbind('MouseOver');
    };
    // 显示并激活按钮功能
    game.enable_button = function(btn, callback, sound = "click_on") {
        if (btn.bg_e) {
            btn.bg_e.alpha = 1;
        }
        btn.e.alpha = 1;
        game.set_button_movement(btn.e, callback, sound);
    };
    /***********************************\
     * panel相关
    \***********************************/
    game.get_trade_panel_show_pct = function(num_cards, card_w, max_pct = 0.8) {
        const max_len = game.sizes.trade_card_r - game.sizes.trade_card_l;
        var show_pct = game.get_show_pct(max_len, num_cards, card_w, max_pct);
        return show_pct;
    }
    game.destroy_cards_e = function(cards) {
        cards.forEach((card, index) => {
            if (card.e) {
                card.e.destroy();
            }
        });
    }
    game.clean_trade_cards = function() {
        game.destroy_cards_e(game.control.trade_pay_cards);
        game.destroy_cards_e(game.control.trade_buy_cards);

        game.control.trade_pay_cards = [];
        game.control.trade_buy_cards = [];
    };

    /***********************************\
     * 设置buy_cards_panel
    \***********************************/
    game.add_buy_card = function(name) {
        var trade_card = {name: name};
        game.control.trade_buy_cards.push(trade_card);
    }
    game.remove_buy_card = function(name, number = 1) {
        var count = 0
        var buy_cards = game.control.trade_buy_cards;
        for( var i = 0; i < buy_cards.length; i++){
            if ( buy_cards[i].name == name && count < number) {
                if (buy_cards[i].e) {buy_cards[i].e.destroy();}
                buy_cards.splice(i, 1);
                count = count + 1;
            }
        }
    }
    game.set_buy_cards_panel = function() {
        console.log("set_buy_cards_panel");
        var buy_cards = game.control.trade_buy_cards;

        buy_cards.sort(game.card_compare);
        const show_pct =  game.get_trade_panel_show_pct(buy_cards.length, game.sizes.trade_card_w);
        game.destroy_cards_e(buy_cards);
        buy_cards.forEach((card, index) => {
            card.e = Crafty.e("2D, DOM, Mouse, card_" + card.name).attr({
                x: game.sizes.trade_card_l + game.sizes.trade_card_w * show_pct * index,
                y: game.sizes.buy_cards_t,
                name: card.name,
                z: 10,
                w: game.sizes.trade_card_w,
                h: game.sizes.trade_card_h,
            }).bind('MouseUp', function(MouseEvent){
                if (game.status.trading_waiting_mode) {
                    return;
                }
                game.remove_buy_card(card.name);
                game.set_buy_cards_panel();
                Crafty.audio.play("click_off", 1, click_volume);
            });
        })
    }


    /***********************************\
     * 设置pay_cards_panel
    \***********************************/
    game.remove_pay_card = function(name) {
        var pay_cards = game.control.trade_pay_cards;
        for( var i = 0; i < pay_cards.length; i++){
            if ( pay_cards[i].name == name) {
                if (pay_cards[i].e) {pay_cards[i].e.destroy();}
                pay_cards.splice(i, 1);
            }
        }
        game.unselect_card(name);
    }
    game.set_pay_cards_panel = function() {
        const selected_cards = game.get_selected_cards();
        const show_pct =  game.get_trade_panel_show_pct(selected_cards.length, game.sizes.trade_card_w);
        game.destroy_cards_e(game.control.trade_pay_cards);
        selected_cards.forEach((card, index) => {
            var trade_card = {name: card.name}
            trade_card.e = Crafty.e("2D, DOM, Mouse, card_" + card.name).attr({
                x: game.sizes.trade_card_l + game.sizes.trade_card_w * show_pct * index,
                y: game.sizes.pay_cards_t,
                // anchor_x: x,
                // anchor_y: y,
                z: 10,
                w: game.sizes.trade_card_w,
                h: game.sizes.trade_card_h,
            }).bind('MouseUp', function(MouseEvent){
                if (game.status.trading_waiting_mode) {
                    return;
                }
                game.remove_pay_card(card.name);
                game.set_pay_cards_panel();
                Crafty.audio.play("click_off", 1, click_volume);
            });
            game.control.trade_pay_cards.push(trade_card);
        })
    };


    /***********************************\
     * 默认界面：结束回合？
    \***********************************/
    game.set_default_button = function() {
        game.disable_trade_mode();
        game.unselect_all_cards();
        game.clean_trade_cards();
        game.control.main_text.e.text("结束回合？");
        game.disable_button(game.control.no_btn);
        if (game.can_buy_development_card()) {
            game.enable_button(game.control.plus_btn, null);
        } else {
            game.disable_button(game.control.plus_btn);
        }

        game.enable_button(game.control.yes_btn, null);

    };

    /***********************************\
     * 发起贸易
    \***********************************/
    game.set_wait_trade_button = function() {
        // game.control.main_text.e.text("取消交易");
        game.control.main_text.e.text("");
        game.enable_button(game.control.no_btn, game.set_default_button, "click_off");
        game.disable_button(game.control.yes_btn);
    };
    game.set_start_trade_button = function() {
        game.control.main_text.e.text("发送贸易请求？");
        game.enable_button(game.control.no_btn, game.set_default_button, "click_off");
        game.enable_button(game.control.yes_btn, game.send_trade_request);
    };

    game.set_select_card_panel_visible = function(visible) {
        game.control.select_card_panel.e.visible = visible;
        game.control.select_card_text.e.visible = visible;
        game.control.button_cards.forEach((card, index) => {
            card.e.visible = visible;
        });
    }
    game.set_buy_pay_card_panel_visible = function(visible) {
        game.control.pay_cards_panel.e.visible = visible;
        game.control.buy_cards_panel.e.visible = visible;
        game.control.trade_mark.e.visible = visible;
    }
    game.set_player_panel_visible = function(visible) {
        game.control.select_player_panel.e.visible = visible;
        game.control.select_player_text.e.visible = visible;
        game.players.forEach((player, index) => {
            if (index != 0) {
                player.e.visible = visible;
                player.frame_e.visible = visible;
            }
        });
    }

    game.send_trade_request = function() {
        game.status.trading_waiting_mode = true;
        game.set_player_panel_visible(true);
        game.set_select_card_panel_visible(false);
        game.set_wait_trade_button();
        Crafty.audio.play("ding");
    }
    game.enable_trade_mode = function() {
        game.status.trading_mode = true;
        game.status.trading_waiting_mode = false;
        game.set_pay_cards_panel();
        game.set_select_card_panel_visible(true);
        game.set_buy_pay_card_panel_visible(true);
    }
    game.disable_trade_mode = function() {
        game.status.trading_mode = false;
        game.status.trading_waiting_mode = false;

        game.set_player_panel_visible(false);
        game.set_select_card_panel_visible(false);
        game.set_buy_pay_card_panel_visible(false);
    }

    /***********************************\
     * load_yn_button
    \***********************************/
    game.load_yn_button = function() {
        const height = game.sizes.panel_h;
        const text_height = game.sizes.panel_h / 3;

        const yn_btn_left = game.sizes.left_panel_w + game.sizes.map_w;
        const yn_btn_top = game.sizes.map_h + text_height;
        const yn_btn_w = game.sizes.right_panel_w / 3.3;
        const yn_btn_h = height - text_height;

        const yn_text_left = yn_btn_left;
        const yn_text_top = game.sizes.map_h;

        // Yes button
        game.control.yes_btn.bg_e = Crafty.e("2D, Canvas, panel").attr({
            x: yn_btn_left,
            y: yn_btn_top,
            z: 0,
            w: yn_btn_w,
            h: yn_btn_h,
        });
        game.control.yes_btn.e = Crafty.e("2D, Canvas, Mouse, button_yes").attr({
            x: yn_btn_left,
            y: yn_btn_top,
            anchor_x: yn_btn_left,
            anchor_y: yn_btn_top,
            z: 0,
            name: 'yes',
            w: yn_btn_w,
            h: yn_btn_h,
        });

        // No button
        game.control.no_btn.bg_e = Crafty.e("2D, Canvas, panel").attr({
            x: yn_btn_left + game.sizes.right_panel_w / 3,
            y: yn_btn_top,
            z: 0,
            w: yn_btn_w,
            h: yn_btn_h,
        });
        game.control.no_btn.e = Crafty.e("2D, Canvas, Mouse, button_no").attr({
            x: yn_btn_left + game.sizes.right_panel_w / 3,
            y: yn_btn_top,
            anchor_x: yn_btn_left + game.sizes.right_panel_w / 3,
            anchor_y: yn_btn_top,
            z: 0,
            name: 'no',
            w: yn_btn_w,
            h: yn_btn_h,
        });

        game.control.main_text.e = Crafty.e("2D, DOM, Text").attr({
                x: yn_text_left, y: yn_text_top, w: game.sizes.right_panel_w, h: text_height})
            .textColor('#338811')
            .textFont({ type: 'italic', family: 'Arial', size: `${text_height/2}px`, weight: 'bold'});
    }

    /***********************************\
     * load_plus_button
    \***********************************/
    game.load_plus_button = function() {
        // 添加技能牌button
        const tl = game.get_card_tl({x: 0, y: 0});
        game.control.plus_btn.e = Crafty.e("2D, Canvas, Mouse, card_dcs_back").attr({
            x: game.sizes.plus_card_x,
            y: tl.y,
            anchor_x: game.sizes.plus_card_x,
            anchor_y: tl.y,
            z: 0,
            name: 'plus',
            w: game.sizes.card_w,
            h: game.sizes.card_h,
        });
    }

    /***********************************\
     * 设置Dice
    \***********************************/
    game.roll_dice = function(e, number) {
        if (e.isPlaying()) {
            return null;
        }
        if (! number) {
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
        Crafty.audio.play("roll_dice");
        return number + 1;
    }

    game.load_dices = function() {
        const dice_left = game.sizes.left_panel_w / 3;
        // const dice_top = map_h + text_height;
        const dice_top = game.sizes.map_h + game.sizes.panel_h * 0.05;
        // const dice_w = game.sizes.left_panel_w / 3;
        const dice_h = game.sizes.panel_h * 0.9; // height - text_height;
        const dice_w = dice_h;

        // Dice button
        dice1 = Crafty.e("2D, Canvas, Mouse, SpriteAnimation, dice1").attr({
            x: dice_left,
            y: dice_top,
            z: 0,
            name: 'dice',
            w: dice_w,
            h: dice_h,
        }).bind('MouseUp', function(MouseEvent){
            const num1 = game.roll_dice(dice1);
            const num2 = game.roll_dice(dice2);
            if (num1 && num2) {
                console.log(num1 + num2);
            }
        });

        // 骰子
        dice2 = Crafty.e("2D, Canvas, Mouse, SpriteAnimation, dice2").attr({
            x: dice_left + dice_w,
            y: dice_top,
            z: 0,
            name: 'dice',
            w: dice_w,
            h: dice_h,
        }).bind('MouseUp', function(MouseEvent){
            const num1 = game.roll_dice(dice1);
            const num2 = game.roll_dice(dice2);
            if (num1 && num2) {
                console.log(num1 + num2);
            }
        });
    }

    /***********************************\
     * load trading panel
    \***********************************/
    game.load_trade_panel = function() {
        const trade_panel_l = game.sizes.left_panel_w + game.sizes.map_w;
        const trade_panel_t = game.sizes.map_h - 4 * game.sizes.panel_h;
        const panel_h = game.sizes.panel_h;
        game.sizes.trade_card_w = game.sizes.card_w;
        game.sizes.trade_card_h = game.sizes.card_h;
        game.sizes.trade_panel_l = trade_panel_l;
        game.sizes.trade_panel_r = trade_panel_l + game.sizes.right_panel_w;
        game.sizes.trade_card_l = game.sizes.trade_panel_l + game.sizes.trade_card_w / 3;
        game.sizes.trade_card_r = game.sizes.trade_panel_r - game.sizes.trade_card_w / 3;

        game.sizes.pay_cards_panel_l = trade_panel_l;
        game.sizes.pay_cards_panel_t = trade_panel_t + panel_h * 3;
        game.sizes.pay_cards_t = game.sizes.pay_cards_panel_t + game.sizes.trade_card_h / 4;

        game.sizes.buy_cards_panel_t = trade_panel_t + panel_h * 2;
        game.sizes.buy_cards_t = game.sizes.buy_cards_panel_t + game.sizes.trade_card_h / 4;


        const select_card_info_text_height = panel_h / 4;
        game.sizes.select_card_panel_t = trade_panel_t + panel_h;
        const select_card_info_text_t = game.sizes.select_card_panel_t + panel_h / 10;
        game.sizes.select_card_t = game.sizes.select_card_panel_t + panel_h / 10 + select_card_info_text_height;

        game.sizes.select_player_panel_t = trade_panel_t + panel_h;
        const select_player_info_text_height = panel_h / 4;
        const select_player_info_text_t = game.sizes.select_player_panel_t + game.sizes.trade_card_h / 4;

        game.sizes.select_player_t = game.sizes.select_player_panel_t + game.sizes.trade_card_h / 4 + select_player_info_text_height;

        const button_card_w = game.sizes.trade_card_w * 4 / 5;
        const button_card_h = game.sizes.trade_card_h * 4 / 5;

        // player select panel
        game.control.select_player_panel.e =Crafty.e("2D, Canvas, panel").attr({
            x: trade_panel_l,
            y: game.sizes.select_player_panel_t,
            z: 0,
            w: game.sizes.right_panel_w,
            h: panel_h,
        });

        game.control.select_player_text.e = Crafty.e("2D, DOM, Text").attr({
                x: game.sizes.trade_card_l,
                y: select_player_info_text_t,
                w: game.sizes.right_panel_w, h: select_player_info_text_height})
            .text("选择你想交易的玩家")
            .textColor('#338811')
            .textFont({ type: 'italic', family: 'Arial', size: `${select_player_info_text_height/2}px`, weight: 'bold'});


        const avatar_size = button_card_w * 0.8;
        const avatar_frame_size = button_card_w;
        const frame_padding = (avatar_frame_size - avatar_size) / 2;
        const panel_padding = avatar_size * 2 / 3;
        game.sizes.trade_avatar_l = game.sizes.trade_panel_l + panel_padding;

        const player_show_pct = game.get_show_pct(
            game.sizes.trade_panel_r - game.sizes.trade_panel_l - panel_padding * 2,
            game.players.length - 1,
            avatar_frame_size,
            1.5,
        );

        game.players.forEach((player, index) => {
            if (index != 0) {
                index = index - 1;
                player.e = Crafty.e("2D, Canvas, Mouse," + player.sprite).attr({
                    x: game.sizes.trade_avatar_l + button_card_w * player_show_pct * index + frame_padding,
                    y: game.sizes.select_player_t + frame_padding,
                    anchor_x: game.sizes.trade_avatar_l + button_card_w * player_show_pct * index + frame_padding,
                    anchor_y: game.sizes.select_player_t + frame_padding,
                    name: player.name,
                    z: 11,
                    w: avatar_size,
                    h: avatar_size,
                })
                player.frame_e = Crafty.e("2D, Canvas, Color").attr({
                    x: game.sizes.trade_avatar_l + button_card_w * player_show_pct * index,
                    y: game.sizes.select_player_t,
                    anchor_x: game.sizes.trade_avatar_l + button_card_w * player_show_pct * index,
                    anchor_y: game.sizes.select_player_t,
                    name: player.name,
                    z: 10,
                    w: avatar_frame_size,
                    h: avatar_frame_size,
                }).color(player.color);

                game.set_button_movement(player.e, null, "click_on", player.frame_e);
            }
        });


        // card select panel
        game.control.select_card_panel.e = Crafty.e("2D, Canvas, panel").attr({
            x: trade_panel_l,
            y: trade_panel_t + panel_h,
            z: 0,
            w: game.sizes.right_panel_w,
            h: panel_h,
        });

        game.control.button_cards = [
            {name: 'lumber'},
            {name: 'brick'},
            {name: 'wool'},
            {name: 'grain'},
            {name: 'ore'},
        ];

        const button_card_show_pct =  game.get_trade_panel_show_pct(
            game.control.button_cards.length, button_card_w, 2
        );
        game.select_buy_card = function(name) {
            return function() {
                if (game.status.trading_mode && !game.status.trading_waiting_mode) {
                    game.add_buy_card(name);
                    game.set_buy_cards_panel();
                }
            }
        }
        game.control.select_card_text.e = Crafty.e("2D, DOM, Text").attr({
                x: game.sizes.trade_card_l,
                y: select_card_info_text_t,
                w: game.sizes.right_panel_w,
                h: select_card_info_text_height
            })
            .text("选择你想获得的牌")
            .textColor('#338811')
            .textFont({ type: 'italic', family: 'Arial', size: `${select_card_info_text_height/2}px`, weight: 'bold'});
        game.control.button_cards.forEach((card, index) => {
            card.e = Crafty.e("2D, Canvas, Mouse, card_" + card.name).attr({
                x: game.sizes.trade_card_l + button_card_w * button_card_show_pct * index,
                y: game.sizes.select_card_t,
                anchor_x: game.sizes.trade_card_l + button_card_w * button_card_show_pct * index,
                anchor_y: game.sizes.select_card_t,
                name: card.name,
                z: 10,
                w: button_card_w,
                h: button_card_h,
            });
            game.set_button_movement(card.e, game.select_buy_card(card.name));
        });

        // my cards to buy
        game.control.buy_cards_panel.e =Crafty.e("2D, Canvas, panel").attr({
            x: trade_panel_l,
            y: trade_panel_t + panel_h * 2,
            z: 0,
            w: game.sizes.right_panel_w,
            h: panel_h,
        });

        const trade_mark_w = panel_h / 3;
        const trade_mark_h = panel_h / 3.5;

        game.control.trade_mark.e =Crafty.e("2D, Canvas, trade").attr({
            x: trade_panel_l + game.sizes.right_panel_w / 2 - trade_mark_w / 2,
            y: trade_panel_t + panel_h * 3 - trade_mark_h / 2,
            z: 1,
            w: trade_mark_w,
            h: trade_mark_h,
        });

        // my cards to pay
        game.control.pay_cards_panel.e =Crafty.e("2D, Canvas, panel").attr({
            x: game.sizes.pay_cards_panel_l,
            y: game.sizes.pay_cards_panel_t,
            z: 0,
            w: game.sizes.right_panel_w,
            h: panel_h,
        });
    }


    /***********************************\
     * load all buttons
    \***********************************/
    game.load_main_button = function() {
        game.load_yn_button();
        game.load_plus_button();
        game.load_dices();
        game.load_trade_panel();
        game.set_default_button();

    }
    return game;
}
