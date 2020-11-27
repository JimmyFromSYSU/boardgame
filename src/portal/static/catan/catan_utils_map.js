
var catan_load_utils_for_map = function(game) {
    // only for internal use
    game.board.points = [];
    game.board.id_to_point = {};
    game.board.edges = [];
    game.board.id_to_edge = {};

    /***********************************\
     * POINT
    \***********************************/
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
    game.point_id_to_loc = function(id) {
        const area = game.board.col * game.board.row;
        var loc = {}
        if (id >= area) {
            loc.z = 1;
            id = id - area;
        } else {
            loc.z = -1;
        }
        loc.x = Math.floor(id % game.board.col);
        loc.y = Math.floor(id / game.board.col);
        return loc;
    }
    game.get_point = function (id) {
        var point = game.board.id_to_point[id];
        if(point) {
            return point;
        } else {
            point = game.point_id_to_loc(id);
            point.id = id;
            game.board.points.push(point);
            game.board.id_to_point[id] = point;
            return point;
        }
    }
    game.get_point_center = function(point) {
        const tile_center = game.get_tile_center({x: point.x, y: point.y});
        const center = {'x': tile_center.x, 'y': tile_center.y + point.z * game.sizes.tile_h / 2};
        return center;
    }


    /***********************************\
     * EDGE
    \***********************************/
    // 计算edge的id
    game.get_edge_id = function(location) {
        const area = game.board.col * game.board.row;
        const xy_id = location.x + location.y * game.board.col;
        return area * (location.z + 1) + xy_id;
    }
    game.edge_id_to_loc = function(id) {
        var loc = {}
        const area = game.board.col * game.board.row;
        loc.z = Math.floor(id / area) - 1;
        id = id - area * (loc.z + 1);
        loc.x = Math.floor(id % game.board.col);
        loc.y = Math.floor(id / game.board.col);
        return loc
    }
    game.get_edge = function (id) {
        var edge = game.board.id_to_edge[id];
        if(edge) {
            return edge;
        } else {
            edge = game.edge_id_to_loc(id);
            game.board.edges.push(edge);
            game.board.id_to_edge[id] = edge;
            return edge;
        }
    }
    game.get_edge_center = function(edge) {
        const tile_center = game.get_tile_center({x: edge.x, y: edge.y});
        const center = {
            'x': tile_center.x - (edge.z == 0 ? game.sizes.tile_w/2 : game.sizes.tile_w/4),
            'y': tile_center.y + (edge.z * game.sizes.tile_h * 3 / 8),
        };
        return center;
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
    return game
}
