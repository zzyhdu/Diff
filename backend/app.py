from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 在这里处理上传文件和执行对账的逻辑
        # ...
        express_file = request.files['expressBill']
        sales_file = request.files['salesData']

        express_bill = pd.read_csv(express_file)
        sales_data = pd.read_csv(sales_file)

        express_bill['快递单号'] = express_bill['快递单号'].astype(str)
        sales_data['快递单号'] = sales_data['快递单号'].astype(str)

        # 使用快递单号进行合并
        merged_data = pd.merge(express_bill, sales_data, on='快递单号', how='outer', indicator=True)

        # 找出在其中一份数据中存在而在另一份数据中缺失的记录
        missing_records = merged_data[merged_data['_merge'] == 'left_only']

        # 打印结果
        # print("匹配成功的记录：")
        # print(merged_data[merged_data['_merge'] == 'both'])

        # print("\n存在异常的记录：")
        # print(missing_records)
        # missing_records.to_csv('存在异常的记录1.csv', index=False)
        

        return send_file(
          io.BytesIO(missing_records.to_csv().encode('utf-8')),
          mimetype='text/csv',
          as_attachment=True,
          download_name='对账结果.csv'
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
