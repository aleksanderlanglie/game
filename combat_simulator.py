import streamlit as st
import random

# Define the player's health and monster's health
player_health = 100
monster_health = 100

# Skill definitions
skills = {
    "Fireball": {"damage": 20, "mana_cost": 10},
    "Ice Shard": {"damage": 15, "mana_cost": 5, "freeze_chance": 0.1},
    "Heal": {"heal_amount": 25, "mana_cost": 8}
}

# Streamlit UI
st.title('Simple Combat Simulator')

# Display health stats
st.write(f"Player Health: {player_health}")
st.write(f"Monster Health: {monster_health}")

# Let the player choose a skill to use
skill_choice = st.selectbox("Choose your skill:", list(skills.keys()))

if st.button('Use Skill'):
    skill = skills[skill_choice]

    if skill_choice == "Heal":
        player_health += skill["heal_amount"]
        st.write(f"You have healed yourself for {skill['heal_amount']} health.")
    else:
        monster_health -= skill["damage"]
        st.write(f"You dealt {skill['damage']} damage to the monster.")

    # Monster's turn to attack
    monster_attack = random.randint(5, 15)
    player_health -= monster_attack
    st.write(f"The monster attacks you back and deals {monster_attack} damage.")

    # Update health stats
    st.write(f"Player Health: {player_health}")
    st.write(f"Monster Health: {monster_health}")

    # Check for end of game
    if player_health <= 0:
        st.error("You have been defeated by the monster.")
    elif monster_health <= 0:
        st.success("You have defeated the monster!")
