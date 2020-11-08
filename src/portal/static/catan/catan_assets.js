/***********************************\
 * 图片文件与大小设置
\***********************************/

var images = {
    'tile': {
        'width': 500,
        'height': 575,
    },
    'card': {
        'width': 284,
        'height': 429,
    },
}


var assets = {
    "audio": {
        "roll_dice": ["/static/sounds/catan/roll_dice.wav"],
        "click_on": ["/static/sounds/catan/click_on.wav"],
        "click_off": ["/static/sounds/catan/click_off.wav"],
        "button_click_on": ["/static/sounds/catan/button_click_on.wav"],
        "button_click_off": ["/static/sounds/catan/button_click_off.wav"],
        "hammering": ["/static/sounds/catan/hammering.wav"],
        "drilling": ["/static/sounds/catan/drilling.wav"],
        "punch": ["/static/sounds/catan/punch.wav"],
        "ding": ["/static/sounds/catan/ding.wav"],
    },
    // "images": ["/static/images/catan/panel/dice.png"],
    "sprites": {
        ///////////////////
        // basic
        //////////////////
        "/static/images/catan/panel/panel.png": {
            "tile": 512,
            "tileh": 240,
            "map": { "panel": [0,0]},
        },
        "/static/images/catan/panel/trade.png": {
            "tile": 645,
            "tileh": 561,
            "map": { "trade": [0,0]},
            // "paddingX": 5,
            // "paddingY": 5,
            // "paddingAroundBorder": 10
        },

        ///////////////////
        // dice
        //////////////////
        // https://www.gettyimages.com/photos/dice?mediatype=photography&phrase=dice&sort=mostpopular
        "/static/images/catan/panel/dice.png": {
            "tile": 1629 / 6,
            "tileh": 270 / 1,
            "map": {
                "dice1": [0,0],
                "dice2": [1,0],
                "dice3": [2,0],
                "dice4": [3,0],
                "dice5": [4,0],
                "dice6": [5,0],
            },
        },

        ///////////////////
        // players
        //////////////////
        "/static/images/user/avatars.jpg": {
            "tile": 580 / 4,
            "tileh": 580 / 4,
            "map": {
                "avatar1": [0,0],
                "avatar2": [1,0],
                "avatar3": [2,0],
                "avatar4": [3,0],
                "avatar5": [0,1],
                "avatar6": [1,1],
            }
        },
        "/static/images/user/0.png": {
            "tile": 225, "tileh": 225, "map": { "player_id_0": [0,0]},
        },
        "/static/images/user/1.jpeg": {
            "tile": 225, "tileh": 225, "map": { "player_id_1": [0,0]},
        },
        "/static/images/user/2.jpeg": {
            "tile": 225, "tileh": 225, "map": { "player_id_2": [0,0]},
        },
        "/static/images/user/3.jpeg": {
            "tile": 225, "tileh": 225, "map": { "player_id_3": [0,0]},
        },
        "/static/images/user/bank.png": {
            "tile": 225, "tileh": 225, "map": { "player_bank": [0,0]},
        },
        ///////////////////
        // tiles
        //////////////////
        "/static/images/catan/map/brick.png": {
            "tile": 500, "tileh": 575, "map": { "tile_brick": [0,0]},
        },
        "/static/images/catan/map/wool.png": {
            "tile": 500, "tileh": 575, "map": { "tile_wool": [0,0]},
        },
        "/static/images/catan/map/ore.png": {
            "tile": 500, "tileh": 575, "map": { "tile_ore": [0,0]},
        },
        "/static/images/catan/map/lumber.png": {
            "tile": 500, "tileh": 575, "map": { "tile_lumber": [0,0]},
        },
        "/static/images/catan/map/grain.png": {
            "tile": 500, "tileh": 575, "map": { "tile_grain": [0,0]},
        },
        "/static/images/catan/map/desert.png": {
            "tile": 500, "tileh": 575, "map": { "tile_desert": [0,0]},
        },
        "/static/images/catan/map/sea.png": {
            "tile": 500, "tileh": 575, "map": { "tile_sea": [0,0]},
        },
        "/static/images/catan/map/land.png": {
            "tile": 500, "tileh": 575, "map": { "tile_land": [0,0]},
        },

        ///////////////////
        // objs
        //////////////////
        "/static/images/catan/map/touch_area.png": {
            "tile": 120, "tileh": 120, "map": { "obj_touch_area": [0,0]},
        },
        "/static/images/catan/map/edge_touch_area.png": {
            "tile": 120, "tileh": 120, "map": { "obj_edge_touch_area": [0,0]},
        },
        // house/town/road https://www.thingiverse.com/thing:3214671
        "/static/images/catan/map/house.png": {
            "tile": 120, "tileh": 120, "map": { "obj_house": [0,0]},
        },
        "/static/images/catan/map/town.png": {
            "tile": 120, "tileh": 120, "map": { "obj_town": [0,0]},
        },
        "/static/images/catan/map/road.png": {
            "tile": 120, "tileh": 120, "map": { "obj_road": [0,0]},
        },
        // https://www.tinkercad.com/things/9ZFl9amBXaA-settlers-of-catan-robber
        "/static/images/catan/map/robber.png": {
            "tile": 120, "tileh": 120, "map": { "obj_robber": [0,0]},
        },

        ///////////////////
        // cards
        //////////////////
        "/static/images/catan/card/brick.png": {
            "tile": 284, "tileh": 429, "map": { "card_brick": [0,0]},
        },
        "/static/images/catan/card/wool.png": {
            "tile": 284, "tileh": 429, "map": { "card_wool": [0,0]},
        },
        "/static/images/catan/card/ore.png": {
            "tile": 284, "tileh": 429, "map": { "card_ore": [0,0]},
        },
        "/static/images/catan/card/lumber.png": {
            "tile": 284, "tileh": 429, "map": { "card_lumber": [0,0]},
        },
        "/static/images/catan/card/grain.png": {
            "tile": 284, "tileh": 429, "map": { "card_grain": [0,0]},
        },
        "/static/images/catan/card/dcs_back.png": {
            "tile": 284, "tileh": 429, "map": { "card_dcs_back": [0,0]},
        },
        "/static/images/catan/card/back.png": {
            "tile": 284, "tileh": 429, "map": { "card_back": [0,0]},
        },
        "/static/images/catan/card/longest_road.png": {
            "tile": 284, "tileh": 429, "map": { "card_longest_road": [0,0]},
        },
        "/static/images/catan/card/maximum_knight.png": {
            "tile": 284, "tileh": 429, "map": { "card_maximum_knight": [0,0]},
        },
        "/static/images/catan/card/score.png": {
            "tile": 284, "tileh": 429, "map": { "card_score": [0,0]},
        },


        ///////////////////
        // button
        //////////////////
        "/static/images/catan/panel/yes.png": {
            "tile": 240, "tileh": 240, "map": { "button_yes": [0,0]},
        },
        "/static/images/catan/panel/no.png": {
            "tile": 240, "tileh": 240, "map": { "button_no": [0,0]},
        },
    },
}
