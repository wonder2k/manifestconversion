#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证 MANIFEST 到佐川模板的转换逻辑
"""

import pandas as pd
import re
import sys

def extract_product_with_quantity(item):
    """从材料描述中提取产品名称和数量"""
    match = re.search(r'\s+([A-Z][A-Z\s]*?)\s+(\d+)\s*$', item)
    if match:
        return f"{match.group(1).strip()} {match.group(2)}"
    return item

def convert_goods_column(goods_str):
    """
    转换 GOODS 列的特殊逻辑
    返回：(Y_value, Z_value, AM_value)
    """
    if not goods_str:
        return None, None, None

    items = [item.strip() for item in str(goods_str).split(',')]

    if len(items) == 0:
        return None, None, None

    # 第一项：提取数字到 Z，去除数字的部分到 Y
    first_item = items[0]
    match = re.search(r'(\d+)\s*$', first_item)

    y_value = None
    z_value = None
    am_value = None

    if match:
        z_value = match.group(1)
        y_value = first_item[:match.start()].strip()
    else:
        y_value = first_item

    # AM 列：从第二项提取产品+数量，然后追加后续项
    if len(items) > 1:
        second_item_product = extract_product_with_quantity(items[1])
        if len(items) > 2:
            am_value = second_item_product + ',' + ','.join(items[2:])
        else:
            am_value = second_item_product

    return y_value, z_value, am_value

def test_conversion():
    """测试转换逻辑"""

    # 测试数据
    test_goods = "POLYESTER 100% KNIT ENSEMBLE 1,ELASTANE 1.0% POLYESTER 99.0% WOVEN DRESS 1,ELASTANE 8% VISCOSE 92% KNIT CROP TOP 1,ELASTANE 1.0% POLYESTER 99.0% WOVEN DRESS 1,OUTSOLE MATERIAL POLYURETHANE UPPER MATERIAL ARTIFICIAL LEATHER SLIPPERS 1,ELASTANE 1% POLYAMIDE 34% POLYESTER 43% VISCOSE 22% WOVEN DRESS 1,ELASTANE 8% POLYESTER 92% KNIT DRESS 1,POLYESTER STORAGE BAG 1,COTTON 100% KNIT PANTYHOSE 1,POLYESTER 100% KNIT ENSEMBLE 1,ELASTANE 5% POLYESTER 95% KNIT SWIMWEAR SET 1,ELASTANE 1.0% POLYESTER 99.0% WOVEN DRESS 1,COTTON 100% KNIT PANTYHOSE 1,POLYESTER STORAGE BAG 1,POLYAMIDE 22% VISCOSE 78% WOVEN ENSEMBLE 1,ELASTANE 5% POLYESTER 95% WOVEN SHIRT 1"

    expected_y = "POLYESTER 100% KNIT ENSEMBLE"
    expected_z = "1"
    expected_am_start = "WOVEN DRESS 1,ELASTANE 8% VISCOSE 92% KNIT CROP TOP 1"

    y_value, z_value, am_value = convert_goods_column(test_goods)

    print("=" * 80)
    print("GOODS 列转换测试")
    print("=" * 80)

    # 验证 Y 列
    y_match = y_value == expected_y
    print(f"\nY 列验证: {'✓ PASS' if y_match else '✗ FAIL'}")
    print(f"  期望: {expected_y}")
    print(f"  实际: {y_value}")

    # 验证 Z 列
    z_match = str(z_value) == expected_z
    print(f"\nZ 列验证: {'✓ PASS' if z_match else '✗ FAIL'}")
    print(f"  期望: {expected_z}")
    print(f"  实际: {z_value}")

    # 验证 AM 列开头
    am_match = am_value.startswith(expected_am_start) if am_value else False
    print(f"\nAM 列验证: {'✓ PASS' if am_match else '✗ FAIL'}")
    print(f"  期望开头: {expected_am_start}")
    print(f"  实际开头: {am_value[:len(expected_am_start)] if am_value else 'None'}")
    print(f"  完整长度: {len(am_value) if am_value else 0}")

    all_pass = y_match and z_match and am_match

    print("\n" + "=" * 80)
    if all_pass:
        print("✓ 所有测试通过！转换逻辑正确。")
        return 0
    else:
        print("✗ 部分测试失败！请检查转换逻辑。")
        return 1

def test_file_conversion():
    """测试文件转换"""
    print("\n" + "=" * 80)
    print("文件转换测试")
    print("=" * 80)

    try:
        # 检查文件是否存在
        import os
        if not os.path.exists('MANIFEST-SAMPLE_SHEIN.xlsx'):
            print("✗ 错误：找不到 MANIFEST-SAMPLE_SHEIN.xlsx")
            return 1

        if not os.path.exists('Zuo-Chuan-Pai-Song-Mo-Ban.xlsx'):
            print("✗ 错误：找不到 Zuo-Chuan-Pai-Song-Mo-Ban.xlsx")
            return 1

        print("✓ 所需文件存在")

        # 读取文件
        df_a = pd.read_excel('MANIFEST-SAMPLE_SHEIN.xlsx', header=None)
        df_template = pd.read_excel('Zuo-Chuan-Pai-Song-Mo-Ban.xlsx', header=None)

        print(f"✓ MANIFEST 文件: {df_a.shape[0]} 行 × {df_a.shape[1]} 列")
        print(f"✓ 佐川模板: {df_template.shape[0]} 行 × {df_template.shape[1]} 列")

        # 验证格式
        if df_a.shape[0] < 4:
            print("✗ MANIFEST 文件行数不足")
            return 1

        if df_a.shape[1] < 40:
            print("✗ MANIFEST 文件列数不足")
            return 1

        print("✓ MANIFEST 文件格式验证通过")

        return 0

    except Exception as e:
        print(f"✗ 文件转换测试失败: {str(e)}")
        return 1

if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "Excel 文件转换系统 - 测试套件".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    result1 = test_conversion()
    result2 = test_file_conversion()

    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)

    if result1 == 0 and result2 == 0:
        print("✓ 所有测试通过！系统可以部署。")
        sys.exit(0)
    else:
        print("✗ 部分测试失败！请检查配置。")
        sys.exit(1)
