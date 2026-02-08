from python_env.lua_env import LuaEnv


def run() -> None:
    env = LuaEnv()
    try:
        obs = env.reset(seed=123)
        unit = next(u for u in obs["units"] if u["id"] == 11)
        start_x, start_y = unit["x"], unit["y"]
        print(f"reset tick={obs['tick']} pos=({start_x},{start_y})")

        for step_index in range(10):
            action = {"unit_id": 11, "dir": "right"}
            obs, reward, done, info = env.step(action)
            unit = next(u for u in obs["units"] if u["id"] == 11)
            print(
                f"step={step_index + 1} tick={obs['tick']} pos=({unit['x']},{unit['y']}) reward={reward} done={done}"
            )
            if done:
                break
    finally:
        env.close()


if __name__ == "__main__":
    run()
