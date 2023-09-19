from mplsoccer import Pitch, Sbopen

# US Women vs Netherland's Women FIFA World Cup 2023
match_id = 3893808
player = "Sophia Olivia Smith"

parser = Sbopen()
df, related, freeze, tactics = parser.event(match_id)

# Boolean mask for filtering dataset by player
team1, team2 = df.team_name.unique()
mask_player = (df.type_name == 'Pass') & (df.player_name == player)

df_player_pass = df.loc[mask_player, ['x', 'y', 'end_x', 'end_y', 'outcome_name', 'pass_assisted_shot_id']]
mask_shot_assist = df_player_pass.pass_assisted_shot_id.notnull()
mask_completed = (df_player_pass.outcome_name.isnull()) & (df_player_pass.pass_assisted_shot_id.isnull())
mask_other = (df_player_pass.outcome_name.notnull()) & (df_player_pass.pass_assisted_shot_id.isnull())

# Set up the pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor('#22312b')

# Plot the passes resulting in a shot
pitch.arrows(df_player_pass[mask_shot_assist].x, df_player_pass[mask_shot_assist].y,
             df_player_pass[mask_shot_assist].end_x, df_player_pass[mask_shot_assist].end_y,
             headwidth=10, headlength=10, color='blue', ax=ax, label='shot assists')

# Plot the completed passes for player
pitch.arrows(df_player_pass[mask_completed].x, df_player_pass[mask_completed].y,
             df_player_pass[mask_completed].end_x, df_player_pass[mask_completed].end_y,
             headwidth=10, headlength=10, color='#ad993c', ax=ax, label='completed passes')

# Plot the other passes
pitch.arrows(df_player_pass[mask_other].x, df_player_pass[mask_other].y,
             df_player_pass[mask_other].end_x, df_player_pass[mask_other].end_y,
             headwidth=10, headlength=10, color='#ba4f45', ax=ax, label='other passes')

# Set up the legend
ax.legend(facecolor='#22312b', handlelength=5, edgecolor='None', fontsize=20, loc='upper left')

# Set the title
ax_title = ax.set_title(f'{player} passes vs {team2}', fontsize=30)

# %%
