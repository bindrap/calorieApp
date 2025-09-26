add this

addition of calories burned
			- figure out equation based on person mass, height, age 
			- also have additonal intensity vairable for 
				- light, moderate, high intensity workout
				- user will have to be honest with themselves here 
					- in future could have this linked to a heart rate monitor to let us know how intense the workout actually was
					- how long you worked out
			- Calories Burned (kcal)=MET×weight_kg×duration_hours
				- `MET` = activity intensity (1 MET = energy used at rest)
				- `weight_kg` = body mass in kilograms
				- `duration_hours` = workout time in hours
				`- User Profile Inputs Needed
					- **Weight** (kg/lbs) → required for equation
					- **Height** (cm/inches) → optional (could use for more accurate BMR / TDEE later)
					- **Age** (years) → optional (affects basal metabolism, not directly MET but useful if you extend)
					- **Gender** (optional, used in some formulas like Harris-Benedict for TDEE)
				- Intensity variables
					- light: 2-3 met
					- med: 4-6 met
					- high: 7-12 met

| Field             | Purpose                      |
| ----------------- | ---------------------------- |
| `id`              | PK                           |
| `user_id`         | Who worked out               |
| `activity_type`   | “Jiu Jitsu”, “Running”, etc. |
| `intensity`       | light / moderate / high      |
| `duration_min`    | Workout time                 |
| `calories_burned` | Stored after calculation     |
| `logged_at`       | Timestamp                    |

| Intensity | Example Activities                                | Approx MET Range |
| --------- | ------------------------------------------------- | ---------------- |
| Light     | Yoga, walking slowly                              | 2–3 MET          |
| Moderate  | Weight training, brisk walking, casual cycling    | 4–6 MET          |
| High      | Running, HIIT, martial arts (like your jiu jitsu) | 7–12+ MET        |
