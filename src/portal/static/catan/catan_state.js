
var catan_load_state = function(game) {
    game.can_move_robber = function() {
        return false
    }

    game.can_build_road = function() {
        return false
    }

    game.can_build_house = function() {
        return false
    }

    game.can_build_town = function() {
        return false
    }

    game.can_roll_dice = function() {
        return false
    }

    game.should_show_text = function() {
        return "结束回合？"
    }

    game.should_show_yes_button = function() {
        return true
    }

    game.should_show_no_button = function() {
        return true
    }

    return game
}
