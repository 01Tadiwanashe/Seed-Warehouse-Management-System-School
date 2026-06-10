# Smart Seed Warehouse Management System

## Default Login Credentials
| Username | Password    | Role    |
|----------|-------------|---------|
| admin    | admin123    | Admin   |
| manager  | manager123  | Manager |
| staff    | staff123    | Staff   |

To change passwords, edit utils/auth.py — update the USERS dictionary.

## Setup in VS Code

1. Open this folder: File > Open Folder > warehouse_app/
2. Open terminal: View > Terminal  (Ctrl + `)
3. python -m venv venv
4. Windows:   venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
5. pip install -r requirements.txt
6. Place your CSV in data/smart_seed_warehouse_dataset.csv
7. Save models from notebook:
     import joblib, os
     os.makedirs('models', exist_ok=True)
     joblib.dump(best_stock_pipe, 'models/stock_model.pkl')
     joblib.dump(best_alert_pipe, 'models/alert_model.pkl')
     joblib.dump(best_reg_pipe,   'models/germ_model.pkl')
8. streamlit run Home.py

## Deploy on Streamlit Community Cloud (Free)

1. Push to GitHub
2. Go to share.streamlit.io
3. Sign in with GitHub > New App
4. Set main file to: Home.py
5. Click Deploy — get a free public URL!
