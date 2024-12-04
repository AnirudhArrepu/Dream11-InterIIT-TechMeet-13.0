import streamlit as st
from datetime import date

# Page Title
st.title("Dream11 Fantasy Team Predictor")
st.markdown("""
    **Welcome to the Dream11 Fantasy Team Predictor!**
    
    Enter the names of 2 teams and select the players from each team.
    Use this tool to get insights and predict an ideal team composition for upcoming matches.
""")

# Team Names in Side-by-Side Columns
st.header("Enter Team Names and Players")
col1, col2 = st.columns(2)

# Team 1 Section
with col1:
    team1_name = st.text_input("Team 1 Name", "")
    st.subheader(f"{team1_name} Players")
    team1_players = [st.text_input(f"Player {i+1} (Team 1)", "") for i in range(11)]

# Team 2 Section
with col2:
    team2_name = st.text_input("Team 2 Name", "")
    st.subheader(f"{team2_name} Players")
    team2_players = [st.text_input(f"Player {i+1} (Team 2)", "") for i in range(11)]

# Match Date Selection
st.header("Enter the Match Date")
match_date = st.date_input(
    "Match Date",
    min_value=date(2000, 1, 1),
    max_value=date.today()
)

# Display the selected date
st.write("Selected Date:", match_date)

# Predict Button
if st.button("Generate Predicted Team"):
    # Ensure both teams have names and 11 players each
    if not team1_name or not team2_name:
        st.warning("Please enter names for both teams.")
    elif len([p for p in team1_players if p]) != 11 or len([p for p in team2_players if p]) != 11:
        st.warning("Each team must have exactly 11 players.")
    else:
        # Placeholder for prediction logic - integrate your model here
        st.success("Generating the Dream Team...")

        # Mock data for illustration purposes - replace with actual model prediction
        dream_team = [
            {"name": f"Player {i+1}", "role": "Batsman", "points": 100 - i * 5}
            for i in range(11)
        ]

        # Display the Dream Team
        st.subheader("Dream Team")
        for i, player in enumerate(dream_team, 1):
            st.write(f"**{i}. {player['name']}** - Role: {player['role']} - Predicted Points: {player['points']}")

        # Optional: Provide additional player insights
        st.markdown("### Player Insights")
        for player in dream_team:
            st.write(f"- **{player['name']}**: {player['role']} with an estimated score of {player['points']} points.")

# Footer
st.markdown("---")
st.caption("Developed for the Dream11 Fantasy Cricket Prediction Challenge.")