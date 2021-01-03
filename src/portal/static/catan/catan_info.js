load_bank_data_to_game = function(bank_data, game) {
    game.info.bank_cards = bank_data['bank_cards']
}

var catan_load_info = function(game) {
    info_sprites = {
        'resource_card': 'card_back',
        'development_card': 'card_dcs_back',
        'score': 'card_score',
        'knight': 'card_maximum_knight',
        'road': 'card_longest_road',
    };
    game.info = {
        resource_card_max_number: 19,
        development_card_max_number: 95,
        bank_cards: [
            {'name': 'lumber', number: 19},
            {'name': 'brick', number: 19},
            {'name': 'wool', number: 19},
            {'name': 'grain', number: 19},
            {'name': 'ore', number: 19},
            {'name': 'dcs_back', number: 95},
        ],
    };

    // 在数字num前补0到size位
    // 如num = 5， size = 2
    // 返回 "05"
    function pad(num, size) {
        num = num.toString();
        while (num.length < size) num = "0" + num;
        return num;
    }

    // 获取银行中卡牌数目的颜色
    // 红色代表市场紧缺，而银行储备充足
    // 绿色代表市场充足，而银行储备不足
    function get_card_number_color(number, max_number){
        if (number == max_number) {
            // 红色
            return '#ff0000'
        } else if (number <= max_number - game.players.length) {
            // 绿色
            return '#00ff00'
        } else {
            // 橙色
            return 'orange'
            // return '#ffff00'
        }
    }

    function get_bank_card_number_color(bank_card) {
        if (bank_card.name == 'dcs_back') {
            return get_card_number_color(bank_card.number, game.info.development_card_max_number);
        } else {
            return get_card_number_color(bank_card.number, game.info.resource_card_max_number);
        }
    }

    game.init_info_action = function() {
        const estimated_bank_info_h = game.sizes.map_h / (game.players.length + 1);
        const max_bank_info_h = game.sizes.left_panel_w / 3;
        const bank_info_h = estimated_bank_info_h < max_bank_info_h
            ? estimated_bank_info_h
            : max_bank_info_h;

        const estimated_player_info_h = game.sizes.map_h / (game.players.length + 1);
        const max_player_info_h = game.sizes.left_panel_w / 3;
        const player_info_h = estimated_player_info_h < max_player_info_h
            ? estimated_player_info_h
            : max_player_info_h;

        const avatar_size = player_info_h / 2;
        const avatar_padding_top = avatar_size / 2;
        const avatar_padding_left = avatar_size / 2;
        const avatar_padding_right = avatar_padding_left;

        const bank_size = bank_info_h / 2;
        const bank_padding_top = bank_size / 2;
        const bank_padding_left = bank_size / 2;
        const bank_padding_right = bank_padding_left;

        const player_frame_padding_lr = game.sizes.left_panel_w / 35;
        const player_frame_padding_td = player_info_h / 60;
        // Bank Panel
        Crafty.e("2D, Canvas, panel").attr({
            x: 0,
            y: 0,
            z: 1,
            w: game.sizes.left_panel_w,
            h: bank_info_h,
        });
        // Bank icon
        Crafty.e("2D, Canvas, player_bank").attr({
            x: bank_padding_left,
            y: bank_padding_top,
            z: 10,
            w: bank_size,
            h: bank_size,
        });


        const bank_card_length = game.sizes.left_panel_w - bank_padding_left - bank_size - bank_padding_right;
        const bank_card_w = bank_card_length /  game.info.bank_cards.length;
        const bank_card_h = game.sizes.card_h / game.sizes.card_w * bank_card_w;
        const bank_card_show_pct =  1;
        const bank_card_number_text_height = bank_info_h / 3;
        const bank_card_padding_top = bank_info_h - bank_card_h - bank_card_number_text_height;

        // Bank cards
        game.info.bank_cards.forEach((bank_card, index) => {
            bank_card.e = Crafty.e("2D, Canvas, card_" + bank_card.name).attr({
                x: bank_padding_left + bank_size + bank_card_w * bank_card_show_pct * index,
                y: bank_card_padding_top,
                z: 10,
                w: bank_card_w,
                h: bank_card_h,
            });
            Crafty.e("2D, DOM, Text").attr({
                x: bank_padding_left + bank_size + bank_card_w * bank_card_show_pct * index + bank_card_w / 4,
                y: bank_card_padding_top + bank_card_h,
                z: 11,
                w: bank_card_w,
                h: bank_card_h
            })
            .text(pad(bank_card.number, 2))
            .textColor(get_bank_card_number_color(bank_card))
            .textFont({family: 'Arial', size: `${bank_card_h / 3}px`, weight: 'bold'});
        });

        // Players panel
        game.players.forEach((player, index) => {
            const panel_padding_ratio = 0.01;
            const d_lr = panel_padding_ratio * game.sizes.left_panel_w;
            const d_td = panel_padding_ratio * player_info_h;
            Crafty.e("2D, Canvas, panel").attr({
                x: d_lr,
                y: bank_info_h + index * player_info_h + d_td,
                z: 1,
                w: game.sizes.left_panel_w - 2 * d_lr,
                h: player_info_h - 2 * d_td,
            });

            Crafty.e("2D, Canvas, Color").attr({
                x: player_frame_padding_lr,
                y: bank_info_h + index * player_info_h + player_frame_padding_td,
                z: 0,
                w: game.sizes.left_panel_w - player_frame_padding_lr * 2,
                h: player_info_h - player_frame_padding_td * 2,
            }).color(player.color);

            Crafty.e("2D, Canvas, Mouse," + player.sprite).attr({
                x: avatar_padding_left,
                y: bank_info_h + index * player_info_h + avatar_padding_top,
                name: player.name,
                z: 10,
                w: avatar_size,
                h: avatar_size,
            });

            info_index = 0;
            const info_card_number_text_height = player_info_h / 3;
            const info_card_padding_top = (
                bank_info_h + player_info_h * (1 + index)
                - bank_card_h - info_card_number_text_height
            );

            const info_card_length = game.sizes.left_panel_w - avatar_padding_left - avatar_size - avatar_padding_right;
            const info_card_w = info_card_length * 0.9 /  Object.entries(game.player.info).length;
            const info_card_h = game.sizes.card_h / game.sizes.card_w * info_card_w;
            const info_card_show_pct = 1;

            for (const [key, value] of Object.entries(player.info)) {
                Crafty.e("2D, Canvas, " + info_sprites[key]).attr({
                    x: avatar_padding_left + avatar_size + info_card_w * info_card_show_pct * info_index + info_card_length * 0.05,
                    y: info_card_padding_top,
                    z: 10,
                    w: info_card_w,
                    h: info_card_h,
                })
                Crafty.e("2D, DOM, Text").attr({
                    x: avatar_padding_left + avatar_size + info_card_w * info_card_show_pct * info_index + info_card_length * 0.05 + info_card_w / 4,
                    y: info_card_padding_top + info_card_h,
                    z: 11,
                    w: info_card_w,
                    h: info_card_h
                })
                .text(pad(value, 2))
                .textColor(player.color)
                .textFont({family: 'Arial', size: `${info_card_h / 3}px`, weight: 'bold'})
                info_index = info_index + 1
            };
        });
    }

    return game
}
