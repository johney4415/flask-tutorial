from app import app

if __name__ == '__main__':
    # debug=True == 修改程式碼直接修改網頁內容
    app.run(debug=True, host='0.0.0.0', port=5050)