var catan_load_players = function(game) {
    game.player = {
        name: '小智',
        id: 1,
        sprite: 'player_id_1',
        color: 'blue',
        info: {
            resource_card: 10,
            development_card: 2,
            score: 3,
            knight: 0,
            road: 5,
        },
    }

    game.players = [
        game.player,
        {
            name: '时涛',
            id: 2,
            sprite: 'player_id_2',
            color: 'red',
            info: {
                resource_card: 5,
                development_card: 1,
                score: 1,
                knight: 1,
                road: 5,
            },
        },
        {
            name: '古今',
            id: 3,
            sprite: 'player_id_3',
            color: 'orange',
            info: {
                resource_card: 10,
                development_card: 0,
                score: 5,
                knight: 0,
                road: 3,
            },
        },
        {
            name: '玩家1', id: 4, sprite: 'avatar3', color: 'yellow',
            info: {
                resource_card: 3,
                development_card: 0,
                score: 2,
                knight: 2,
                road: 2,
            },
        },
        // {name: '玩家2', id: 5, sprite: 'avatar2', color: 'green',},
        // {name: '玩家3', id: 6, sprite: 'avatar1', color: 'purple',},
        // {name: '小智', id: 7, sprite: 'player_id_1', color: 'purple',},
        // {name: '时涛', id: 8, sprite: 'player_id_2', color: 'black',},
    ]
    return game
}
