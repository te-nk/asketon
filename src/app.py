import ui
import db
from actions import cloud, workout, version, menu, tasks, finance

ACTIONS = {
    "v": version.run,
    "c": cloud.run,
    "w": workout.run,
    "t": tasks.run,
    "f": finance.run
}
        
def run():
    
    db.init_db()

    while True:
        
        ui.clear_screen()
        menu.run()

        key = ui.read_key().lower()
            
        if key == "q":
            ui.render_out()
            ui.clear_screen()
            break
            
        action = ACTIONS.get(key)
        if action:
            ui.render_out()
            ui.clear_screen()
            action()

if __name__ == "__main__":
    run()
