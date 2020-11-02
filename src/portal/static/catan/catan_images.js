/***********************************\
 * 图片文件与大小设置
\***********************************/

var images = {
    'tile': {
        'files': {
            'brick': '/static/images/catan/map/brick.png',
            'wool': '/static/images/catan/map/wool.png',
            'ore': '/static/images/catan/map/ore.png',
            'lumber': '/static/images/catan/map/lumber.png',
            'grain': '/static/images/catan/map/grain.png',
            'desert': '/static/images/catan/map/desert.png',
            'sea': '/static/images/catan/map/sea.png',
            'land': '/static/images/catan/map/land.png',
        },
        'width': 500,
        'height': 575,
    },
    'obj': {
        // More: https://dribbble.com/shots/9246072-Wood-Catan-3
        'files': {
            'touch_area': '/static/images/catan/map/touch_area.png',
            'edge_touch_area': '/static/images/catan/map/edge_touch_area.png',
            // house/town/road https://www.thingiverse.com/thing:3214671
            'house': '/static/images/catan/map/house.png',
            'town': '/static/images/catan/map/town.png',
            'road': '/static/images/catan/map/road.png',
            // https://www.tinkercad.com/things/9ZFl9amBXaA-settlers-of-catan-robber
            'robber': '/static/images/catan/map/robber.png',
        },
        'width': 120,
        'height': 120,
    },
    'card': {
        'files': {
            'brick': '/static/images/catan/card/brick.png',
            'wool': '/static/images/catan/card/wool.png',
            'ore': '/static/images/catan/card/ore.png',
            'lumber': '/static/images/catan/card/lumber.png',
            'grain': '/static/images/catan/card/grain.png',
            'dcs_back': '/static/images/catan/card/dcs_back.png',
        },
        'width': 284,
        'height': 429,
    },
    'button': {
        'files': {
            'yes': "/static/images/catan/panel/yes.png",
            'no': "/static/images/catan/panel/no.png",
            'plus': "/static/images/catan/panel/plus.png",
        },
        'width': 240,
        'height': 240,
    },
    'player': {
        'files': {
            'id_1': "/static/images/user/1.jpeg",
            'id_2': "/static/images/user/2.jpeg",
            'id_3': "/static/images/user/3.jpeg",
        },
        'width': 240,
        'height': 240,
    },
}

var panel_image_file = "/static/images/catan/panel/panel.png";
var panel_image_w = 512;
var panel_image_h = 240;


// https://www.gettyimages.com/photos/dice?mediatype=photography&phrase=dice&sort=mostpopular
var dice_image_file = "/static/images/catan/panel/dice.png";
var dice_image_w = 1629;
var dice_image_h = 270;
var single_dice_image_w = dice_image_w / 6;
var single_dice_image_h = dice_image_h / 1;


var trade_image_file = "/static/images/catan/panel/trade.png";
var trade_image_w = 645;
var trade_image_h = 561;
