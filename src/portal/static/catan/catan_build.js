/***********************************\
* Build House/Town/Road
\***********************************/

var catan_load_build = function(game) {
    /***********************************\
     * ROAD
    \***********************************/
    game.build_road = function(loc) {
        var id = game.get_edge_id({
            x: loc.x,
            y: loc.y,
            z: loc.z,
        })
        var edge = game.get_edge(id)
        edge.name = 'house'
        const center = game.get_edge_center(edge)
        const rotation = (loc.z == 0 ? 90 : 30 * loc.z);
        const w = game.sizes.tile_h/2
        const h = game.sizes.tile_h/4
        edge.e = Crafty.e(`2D, DOM, obj_road`).attr({
            x: center.x - w/2,
            y: center.y - h/2,
            z: 3,
            alpha: 1,
            w: w,
            h: h,
        }).origin('center');
        edge.e.rotation = rotation;

        // TODO: 统一管理哪些touch_e能够被点击
        if (edge.touch_e) {
            edge.touch_e.unbind('Click')
        }
    }

    game.build_road_action = function(loc) {
        game.build_road(loc)
        Crafty.audio.play("hammering", 1, game.click_volume);
    }

    /***********************************\
     * HOUSE
    \***********************************/
    game.build_house = function(loc) {
        var id = game.get_point_id({
            x: loc.x,
            y: loc.y,
            z: loc.z,
        })
        var point = game.get_point(id)
        point.name = 'house'
        const center = game.get_point_center(point)
        const w = game.sizes.tile_h / 4
        const h = game.sizes.tile_h / 4
        point.e = Crafty.e(`2D, DOM, obj_house`).attr({
            x: center.x - w/2,
            y: center.y - h/2,
            z: 4,
            alpha: 1,
            w: w,
            h: h,
        })
    }
    game.build_house_action = function(loc) {
        game.build_house(loc)
        Crafty.audio.play("hammering", 1, game.click_volume)
    }

    /***********************************\
     * TOWN
    \***********************************/
    game.build_town = function(loc) {
        var id = game.get_point_id({
            x: loc.x,
            y: loc.y,
            z: loc.z,
        })
        var point = game.get_point(id)
        const center = game.get_point_center(point)
        const w = game.sizes.tile_h / 4
        const h = game.sizes.tile_h / 4
        var house_e = point.e
        point.name = 'town'
        point.e = Crafty.e(`2D, DOM, obj_town`).attr({
            x: center.x - w * 3 / 4,
            y: center.y - h * 3 / 4,
            z: 5,
            alpha: 1,
            w: w * 1.4,
            h: h * 1.4,
        })

        // TODO: 统一管理哪些touch_e能够被点击
        if (point.touch_e) {
            point.touch_e.unbind('Click')
        }

        house_e.destroy()

    }
    game.build_town_action = function(loc) {
        game.build_town(loc)
        Crafty.audio.play("drilling", 1, game.click_volume)
    }

    return game
}
