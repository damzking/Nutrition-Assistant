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

## Deploy the Flask API to Render

1. In Render, create a new Blueprint and select this GitHub repository. Render
   will use [`render.yaml`](render.yaml) to build and start the API.
2. Set `deepseek_api_key`, `SUPABASE_URL`, and `SUPABASE_SECRET_KEY` as secret
   environment variables for the Flask service in Render. Do not put these
   values in GitHub or in the Streamlit app.
3. Wait for the deploy to finish, then open
   `https://<your-render-service>.onrender.com/health`. A healthy service
   returns `{"status":"ok"}`.
4. Configure the Streamlit app's `FLASK_API_URL` to the Render service's base
   URL as described below.

The health endpoint only checks that Flask is responding; it does not make
requests to DeepSeek or Supabase.

## Deploy the Streamlit app to Community Cloud

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with the
   GitHub account that can access this repository.
2. Select **Create app**, choose this repository and the `main` branch, and set
   the app file path to `streamlit_app.py`.
3. Before deploying, open the app's **Advanced settings** and add the following
   under **Secrets**, replacing the URL with your Render service's base URL:

   ```toml
   FLASK_API_URL = "https://<your-render-service>.onrender.com"
   ```

4. Deploy the app. It should open with the Flask API address prefilled. Upload
   an image and select **Analyse image** to verify the end-to-end connection.

Only the Flask API URL belongs in Streamlit settings. Keep the DeepSeek API key
and Supabase secret key configured on Render, not in this app or its repository.
