-- Calorie Tracker Database Schema
-- SQLite database for MVP version

-- Users table for multi-user support
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Food database table (from USDA or other sources)
CREATE TABLE food_database (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name VARCHAR(200) NOT NULL,
    food_code VARCHAR(50), -- USDA food code if available
    calories_per_100g DECIMAL(8,2) NOT NULL,
    protein_per_100g DECIMAL(8,2) DEFAULT 0,
    carbs_per_100g DECIMAL(8,2) DEFAULT 0,
    fat_per_100g DECIMAL(8,2) DEFAULT 0,
    fiber_per_100g DECIMAL(8,2) DEFAULT 0,
    sugar_per_100g DECIMAL(8,2) DEFAULT 0,
    sodium_per_100g DECIMAL(8,2) DEFAULT 0,
    category VARCHAR(100), -- fruits, vegetables, grains, etc.
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Food entries (user's logged meals)
CREATE TABLE food_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_name VARCHAR(200) NOT NULL,
    estimated_weight_grams DECIMAL(8,2), -- AI estimated portion size
    actual_weight_grams DECIMAL(8,2), -- user corrected portion size
    calories DECIMAL(8,2) NOT NULL,
    protein DECIMAL(8,2) DEFAULT 0,
    carbs DECIMAL(8,2) DEFAULT 0,
    fat DECIMAL(8,2) DEFAULT 0,

    -- AI analysis results
    ai_confidence_score DECIMAL(3,2), -- 0.0 to 1.0
    ai_identified_foods TEXT, -- JSON array of identified foods

    -- User corrections
    user_corrected BOOLEAN DEFAULT FALSE,
    original_ai_food_name VARCHAR(200), -- what AI initially identified

    -- Image information
    image_filename VARCHAR(255),
    image_path VARCHAR(500),

    -- Timing
    consumed_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- User daily goals (optional for future enhancement)
CREATE TABLE user_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    daily_calorie_goal INTEGER DEFAULT 2000,
    daily_protein_goal DECIMAL(8,2) DEFAULT 50,
    daily_carbs_goal DECIMAL(8,2) DEFAULT 250,
    daily_fat_goal DECIMAL(8,2) DEFAULT 65,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_food_entries_user_id ON food_entries(user_id);
CREATE INDEX idx_food_entries_consumed_at ON food_entries(consumed_at);
CREATE INDEX idx_food_database_name ON food_database(food_name);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Sample data for food_database (basic items)
INSERT INTO food_database (food_name, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, category) VALUES
('Apple', 52, 0.3, 14, 0.2, 'fruits'),
('Banana', 89, 1.1, 23, 0.3, 'fruits'),
('Rice (cooked)', 130, 2.7, 28, 0.3, 'grains'),
('Chicken Breast', 165, 31, 0, 3.6, 'protein'),
('Broccoli', 34, 2.8, 7, 0.4, 'vegetables'),
('Bread (white)', 265, 9, 49, 3.2, 'grains'),
('Egg', 155, 13, 1.1, 11, 'protein'),
('Salmon', 208, 20, 0, 13, 'protein'),
('Pasta (cooked)', 131, 5, 25, 1.1, 'grains'),
('Milk (whole)', 61, 3.2, 4.8, 3.3, 'dairy');