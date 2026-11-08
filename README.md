# Nutrition Assistant

A Streamlit interface backed by a Flask API. Flask sends uploaded meal images
to DeepSeek for nutrition estimates and saves the results to Supabase.

## Local setup

1. Install Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your DeepSeek and Supabase credentials.
   Keep `.env` private; the Supabase secret key belongs on the Flask server only.

3. In the Supabase SQL Editor, run [`database/supabase_schema.sql`](database/supabase_schema.sql).

4. Start Flask from the project root:

   ```powershell
   python app.py
   ```

5. In a second terminal, start Streamlit:

   ```powershell
   python -m streamlit run streamlit_app.py
   ```

By default, Streamlit connects to Flask at `http://127.0.0.1:5000`. Set
`FLASK_API_URL` if the Flask API is hosted at a different address.

Uploaded images are analyzed in memory and are not saved to Supabase. The
nutrition results are inserted into the `public.nutrition_analyses` table.
