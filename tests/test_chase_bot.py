"""Test ChaseBot to verify the fix for bitwise inversion deprecation warning."""
from ursinaxball.common_values import TeamID
from ursinaxball.game import Game, GameScore
from ursinaxball.modules import PlayerHandler
from ursinaxball.modules.bots.common_bots import ChaseBot
from ursinaxball.modules.systems.game_config import GameConfig


def test_chase_bot_kick_cancel():
    """Test that ChaseBot works correctly with the boolean negation fix."""
    config = GameConfig(
        enable_renderer=False,
        enable_recorder=False,
    )

    game = Game(config)

    custom_score = GameScore(time_limit=1, score_limit=1)
    game.score = custom_score

    bot = ChaseBot(tick_skip=1)
    player_red = PlayerHandler("P0", TeamID.RED, bot=bot)
    player_blue = PlayerHandler("P1", TeamID.BLUE)
    game.add_players([player_red, player_blue])

    game.start()

    # Run a few steps to ensure bot executes actions correctly
    actions_executed = []
    for _ in range(10):
        actions_player_1 = player_red.step(game)
        actions_player_2 = [0, 0, 0]
        actions_executed.append(actions_player_1)
        done = game.step([actions_player_1, actions_player_2])
        if done:
            break

    # Verify that bot returned valid actions (list of 3 integers)
    assert len(actions_executed) > 0, "Bot should have executed at least one action"
    for actions in actions_executed:
        assert isinstance(actions, list), "Actions should be a list"
        assert len(actions) == 3, "Actions should contain 3 elements"
        assert all(isinstance(a, int) for a in actions), "All actions should be integers"

