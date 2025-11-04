from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import re
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_manifest_format(df):
    """
    Validate if the uploaded file is in MANIFEST format
    Check:
    1. File should have data
    2. Row 4 (index 3) should have mapping indicators
    3. File should have at least columns up to column I
    """
    if df.shape[0] < 4 or df.shape[1] < 9:
        return False, "文件格式错误：行数或列数不足"

    # Check if row 4 (index 3) has any non-NaN values (mapping row)
    mapping_row = df.iloc[3]
    has_mapping = mapping_row.notna().any()

    if not has_mapping:
        return False, "文件格式错误：第4行缺少转换规则标注"

    return True, "格式验证通过"

def convert_file_a_to_b(input_df, template_file_path='Zuo-Chuan-Pai-Song-Mo-Ban.xlsx'):
    """
    Convert File A (MANIFEST) to File B (Zuo Chuan) format with corrected GOODS logic
    """
    try:
        # Validate format
        is_valid, message = validate_manifest_format(input_df)
        if not is_valid:
            return None, message

        # Read template
        df_template = pd.read_excel(template_file_path, header=None)

        # Determine output columns
        max_col_needed = 39
        num_cols = max(df_template.shape[1], max_col_needed)

        # Initialize output with template header
        output_rows = [df_template.iloc[0].tolist() + [None] * (num_cols - df_template.shape[1])]

        # Column mapping (File A column index -> File B column index)
        column_mapping = {
            4: 0,   # HOUSE AIR WAYBILL NO. -> A
            6: 22,  # WEIGHT -> W
            9: 28,  # IMPORT NAME -> AC
            11: 29, # TEL NO. -> AD
            12: 15, # SHIPPER NAME -> P
            15: 27, # DECLARED VALUE OF CUSTOMS -> AB
            19: 34, # CONSIGNEE ZIP -> AI
            37: 35, # SKU -> AJ
            38: 36, # 商品链接 -> AK
            39: 37, # HS CODE -> AL
        }

        # Process each data row (starting from row 2 in Excel, index 1)
        for row_idx in range(1, input_df.shape[0]):
            # Skip empty rows and special rows
            if row_idx == 2 or row_idx == 3:
                continue

            # Create new row
            new_row = [None] * num_cols

            # Copy mapped columns
            for src_col, dest_col in column_mapping.items():
                if src_col < input_df.shape[1]:
                    value = input_df.iloc[row_idx, src_col]
                    new_row[dest_col] = value if pd.notna(value) else None

            # Special handling for column I (index 8) - GOODS with CORRECTED LOGIC
            goods_value = input_df.iloc[row_idx, 8]
            if pd.notna(goods_value):
                goods_str = str(goods_value)
                items = [item.strip() for item in goods_str.split(',')]

                if len(items) > 0:
                    # First item: extract number to Z, text without number to Y
                    first_item = items[0]
                    match = re.search(r'(\d+)\s*$', first_item)
                    if match:
                        z_value = match.group(1)
                        y_value = first_item[:match.start()].strip()
                        new_row[25] = z_value  # Z column (index 25)
                        new_row[24] = y_value  # Y column (index 24)
                    else:
                        new_row[24] = first_item

                    # AM column: extract product+qty from item 2, then append items 3+
                    if len(items) > 1:
                        # Extract product and quantity from second item
                        second_item = items[1]
                        match = re.search(r'\s+([A-Z][A-Z\s]*?)\s+(\d+)\s*$', second_item)
                        if match:
                            product_qty = f"{match.group(1).strip()} {match.group(2)}"
                        else:
                            product_qty = second_item

                        # Build AM column
                        if len(items) > 2:
                            am_value = product_qty + ',' + ','.join(items[2:])
                        else:
                            am_value = product_qty

                        new_row[38] = am_value  # AM column (index 38)

            output_rows.append(new_row)

        # Create output dataframe
        df_output = pd.DataFrame(output_rows)
        return df_output, "转换成功"

    except Exception as e:
        return None, f"转换出错: {str(e)}"

@app.route('/api/convert', methods=['POST'])
def convert():
    """API endpoint for file conversion"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有文件被上传'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'message': '文件名为空'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': '只支持 Excel 文件 (.xlsx 或 .xls)'}), 400

        # Read uploaded file
        try:
            input_df = pd.read_excel(file, header=None)
        except Exception as e:
            return jsonify({'success': False, 'message': f'无法读取 Excel 文件: {str(e)}'}), 400

        # Convert file
        output_df, message = convert_file_a_to_b(input_df)

        if output_df is None:
            return jsonify({'success': False, 'message': message}), 400

        # Write to BytesIO
        output = io.BytesIO()
        output_df.to_excel(output, header=False, index=False, engine='openpyxl')
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'Zuo-Chuan-Converted-{pd.Timestamp.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        )

    except Exception as e:
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'}), 500

@app.route('/api/validate', methods=['POST'])
def validate():
    """API endpoint for file format validation"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有文件被上传'}), 400

        file = request.files['file']
        input_df = pd.read_excel(file, header=None)
        is_valid, message = validate_manifest_format(input_df)

        return jsonify({'success': is_valid, 'message': message})

    except Exception as e:
        return jsonify({'success': False, 'message': f'验证失败: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
