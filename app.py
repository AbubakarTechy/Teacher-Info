from flask import Flask, render_template, request
import pandas as pd, os

app = Flask(__name__)

DATA_CSV = os.path.join(os.path.dirname(__file__), 'teachers.csv')
df = pd.read_csv(DATA_CSV).fillna('')
# Normalize image extensions to lowercase to avoid case-sensitivity issues
df['picture_url'] = df['picture_url'].apply(
    lambda u: u[:u.rfind('.')] + u[u.rfind('.'):].lower() if '.' in u else u
)

@app.route('/')
def home():
    sample = df.head(8).to_dict(orient='records')
    return render_template('index.html', teachers=sample)

@app.route('/search', methods=['POST'])
def search():
    q = request.form.get('name', '').strip()
    if not q:
        return render_template('result.html', teacher_list=[], query=q)
    matches = df[df['name'].str.contains(q, case=False, na=False)].to_dict(orient='records')
    return render_template('result.html', teacher_list=matches, query=q)

# --- FIXED: Lookup teacher by email ---
@app.route('/teacher/<email>')
def teacher_detail(email):
    row = df[df['email'] == email]
    if not row.empty:
        teacher = row.iloc[0].to_dict()
        return render_template('teacher.html', teacher=teacher)
    else:
        return "Teacher not found", 404

@app.route('/all_teachers')
def all_teachers():
    teachers = df.to_dict(orient='records')
    return render_template('all_teachers.html', teachers=teachers)

if __name__ == '__main__':
    app.run(debug=True)
