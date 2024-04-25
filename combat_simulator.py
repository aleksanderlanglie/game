import streamlit as st
import random
import time

# Define the player's initial stats
player_health = 100
player_mana = 50

# Skill definitions
skills = {
    "Fireball": {"damage": 20, "mana_cost": 10},
    "Ice Shard": {"damage": 15, "mana_cost": 5, "freeze_chance": 0.1},
    "Heal": {"heal_amount": 25, "mana_cost": 8}
}

# Streamlit UI
st.title('Simple Combat Simulator')

# Pre-combat skill and condition setup
st.subheader('Choose your skill and condition for auto-trigger:')
chosen_skill = st.selectbox("Select a skill:", list(skills.keys()))
trigger_health = st.slider("Trigger skill when health below (%):", 0, 100, 30)

# Layout for player and monster stats
col1, col2 = st.columns(2)
with col1:
    st.write("Player")
    player_health_bar = st.progress(player_health)
    player_health_text = st.empty()
    player_mana_bar = st.progress(player_mana)
    player_mana_text = st.empty()

# Function to spawn a new monster
def spawn_monster():
    return 100, 50  # Health and Mana

monster_health, monster_mana = spawn_monster()

with col2:
    st.write("Monster")
    monster_health_bar = st.progress(monster_health)
    monster_health_text = st.empty()
    monster_mana_bar = st.progress(monster_mana)
    monster_mana_text = st.empty()

def update_health_bars():
    # Clamp values between 0 and 100 before updating
    clamped_player_health = max(0, min(100, player_health))
    clamped_player_mana = max(0, min(100, player_mana))
    clamped_monster_health = max(0, min(100, monster_health))
    clamped_monster_mana = max(0, min(100, monster_mana))

    player_health_bar.progress(clamped_player_health)
    player_health_text.text(f"Health: {clamped_player_health}")
    player_mana_bar.progress(clamped_player_mana)
    player_mana_text.text(f"Mana: {clamped_player_mana}")

    monster_health_bar.progress(clamped_monster_health)
    monster_health_text.text(f"Health: {clamped_monster_health}")
    monster_mana_bar.progress(clamped_monster_mana)
    monster_mana_text.text(f"Mana: {clamped_monster_mana}")

# Start the combat loop
if st.button('Start Combat'):
    st.session_state['combat_active'] = True

while 'combat_active' in st.session_state and st.session_state['combat_active']:
    time.sleep(3)  # Wait for 3 seconds between rounds

    # Player's automatic attack
    monster_health -= 10
    update_health_bars()
    st.write("Player attacks monster for 10 damage.")
    
    if player_health <= trigger_health:
        skill = skills[chosen_skill]
        if chosen_skill == "Heal" and player_mana >= skill["mana_cost"]:
            player_health += skill["heal_amount"]
            player_mana -= skill["mana_cost"]
            st.write(f"Triggered {chosen_skill} healing yourself for {skill['heal_amount']} health.")
        elif player_mana >= skill["mana_cost"]:
            monster_health -= skill["damage"]
            player_mana -= skill["mana_cost"]
            st.write(f"Triggered {chosen_skill} dealing {skill['damage']} damage to the monster.")
        update_health_bars()

    # Monster's turn to attack
    monster_attack = random.randint(5, 15)
    player_health -= monster_attack
    update_health_bars()
    st.write(f"The monster attacks you back and deals {monster_attack} damage.")

    # Check for end of game
    if player_health <= 0:
        st.error("You have been defeated by the monster.")
        st.session_state['combat_active'] = False  # Stop the combat loop
    elif monster_health <= 0:
        st.success("You have defeated the monster!")
        monster_health, monster_mana = spawn_monster()  # Spawn new monster
        update_health_bars()  # Update health bars to new monster stats
