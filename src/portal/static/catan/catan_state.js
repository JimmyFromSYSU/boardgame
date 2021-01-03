
var catan_load_state = function(game) {
    game.can_move_robber = function() {
        return false
    }

    game.can_build_road = function() {
        return true
    }

    game.can_build_house = function() {
        console.log(`state: ${game.state}, curr_player:${game.current_player_id} user_id: ${game.user_id}`)
        if (game.state == 'START' && game.current_player_id.toString() == game.user_id) {
            return true
        }
        return false
    }

    game.can_build_town = function() {
        return game.can_build_house()
    }

    game.can_roll_dice = function() {
        return false
    }

    game.should_show_text = function() {
        // return "结束回合？"
        return "请放置一所房子"
    }

    game.should_show_yes_button = function() {
        return false
    }

    game.should_show_no_button = function() {
        return false
    }

    game.update_ui = function() {

    }

    return game
}
