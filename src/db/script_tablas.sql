CREATE TABLE IF NOT EXISTS matches (
	match_id SERIAL PRIMARY KEY,
	season INT NOT NULL,
	league_match INT NOT NULL,
	team_1 VARCHAR(50) NOT NULL,
	team_2 VARCHAR(50) NOT NULL, 
);

CREATE TABLE IF NOT EXISTS ranking (
	rank_id SERIAL PRIMARY KEY,
	season INT NOT NULL,
	league_match INT NOT NULL,
	team VARCHAR(50) NOT NULL,
	home_wins INT NOT NULL,
	away_wins INT NOT NULL,
	home_losses INT NOT NULL,
	away_losses INT NOT NULL,
	home_draws INT NOT NULL,
	away_draws INT NOT NULL,
	goals_scored INT NOT NULL,
	goals_conceded INT NOT NULL,
	win_streak INT NOT NULL,
	draw_streak INT NOT NULL,
	loss_streak INT NOT NULL
);
