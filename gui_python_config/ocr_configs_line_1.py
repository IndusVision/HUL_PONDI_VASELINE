import json
import sys
import os

ROOT_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

def rel_path(*paths):
    return os.path.join(ROOT_DIR, *paths)

def save_ocr_config(config):
    config_path = rel_path("gui_python_config", "Line_1_Code_Config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)  # <-- FIX

    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)

    print(f"OCR Configuration saved to {config_path}")
    
def update_ocr_config(sku):
    sku = int(sku)
    ocr_configs_line_1 = {
        1: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","100ml","line_1_100ml_after_filling.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","line_1_fp_before_filling_100ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","nea_korea_100ml.Config"),

            "camera_serial_number": "054003520047",
            "default_conf": 0.2, 
            "iou_thersh": 0.5,
            "ocr_count": 8,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":3,
            "ocr_weights":rel_path("Models","code_on_bottom_best.pt"),
            "product_id":"38",
            "sku_id":"Japan_80gm"},  # japan 80


        2: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","250ml","line_1_fp_after_filling_250ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","Line_1_fp_before_filling_250ml.Config"),

            "camera_config_ocr":rel_path("vaseline_line_1","Config_Files","line_1_Japan_200gm.Config"),

            "camera_serial_number": "054003520047",
            "default_conf": 0.4,
            "iou_thersh": 0.7,
            "ocr_count": 9,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":2,
            "ocr_weights":rel_path("Models","code_on_bottom_best.pt"),
            "product_id":"37",
            "sku_id": "Japan_200gm"},  # Japan 200


        3: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","100ml","line_1_100ml_after_filling.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","line_1_fp_before_filling_100ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","singapore 100 ml.Config"),

            "camera_serial_number":"054003520047",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":3,
            "ocr_weights":rel_path("Models","code_on_cap_best.pt"),
            "product_id":"44",
            "sku_id":"Europe_100ml"},  # europe 100


        4: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","250ml","line_1_fp_after_filling_250ml.Config"),
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","Line_1_fp_before_filling_250ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","europe_200ml.Config"),
            
            "camera_serial_number":"054003520047",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":2,
            "ocr_weights":rel_path("Models","code_on_cap_best.pt"),
            "product_id":"38",
            "sku_id":"Europe_250ml"},  # europe250


        5: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","100ml","line_1_100ml_after_filling.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","line_1_fp_before_filling_100ml.Config"),

            "camera_config_ocr":rel_path("vaseline_line_1","Config_Files","Line1_OCR","singapore 100 ml.Config"),

            "camera_serial_number":"054003520047",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 9,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":3,
            "ocr_weights":rel_path("Models","code_on_cap_best.pt"),
            "product_id":"35",
            "sku_id":"Singapore_100ml"},  # singapore 100


        6: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","250ml","line_1_fp_after_filling_250ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","Line_1_fp_before_filling_250ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","Singapore_250ml.Config"), 

            "camera_serial_number":"054003520047",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":2,
            "ocr_weights":rel_path("Models","code_on_cap_best.pt"),
            "product_id":"36",
            "sku_id": "Singapore_250ml"},    #singapore 250


        7: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","100ml","line_1_100ml_after_filling.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","line_1_fp_before_filling_100ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","nea_korea_100ml.Config"),

            "camera_serial_number": "054003520047",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 9,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":3,
            "ocr_weights": rel_path("Models","code_on_cap_best.pt"),
            "product_id":"41",
            "sku_id":"NEA_Hongkong_100ml"}, #nea hongkong_100ml


        8: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","100ml","line_1_100ml_after_filling.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","line_1_fp_before_filling_100ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","nea_korea_100ml.Config"),

            "camera_serial_number": "054003520047", 
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 13,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":3,
            "ocr_weights": rel_path("Models","code_on_sticker_16_july_best.pt"),
            "product_id":39,
            "sku_id":"NEA_KOREA_100ml"},    #nea korea 100ml


         9: {"camera_config_After_filling":rel_path("vaseline_line_1","Config_Files","Line_1_fp_after_filling","100ml","line_1_100ml_after_filling.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_1","Config_Files","Line1_fp_before_filling","line_1_fp_before_filling_100ml.Config"),

            "camera_config_ocr": rel_path("vaseline_line_1","Config_Files","Line1_OCR","nea_korea_100ml.Config"), #singapore100ml

            "camera_serial_number": "054003520047",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 0,
            "recipe_start_offset":0,
            "recipe_bit_offset":3,
            "ocr_weights":rel_path("Models","code_on_cap_best.pt"),
            "product_id":"36",
            "sku_id": "Singapore_250ml"},    #Australia 100

        # 3: {"camera_config_After_filling":"C:/Users/pc/Desktop/Config_Files/Line_1_fp_after_filling/100ml/line_1_100ml_after_filling.Config",
        #     "camera_config_before_filling":"C:/Users/pc/Desktop/Config_Files/Line1_fp_before_filling/line_1_fp_before_filling_100ml.Config",
        #     "camera_config_ocr":  "C:/Users/pc/Desktop/Config_Files/Line1_OCR/Line1_singapore 100 ml_OCR.Config", "camera_serial_number":"0540035320047",
        #     "default_conf": 0.5,
        #     "iou_thersh": 0.75,
        #     "ocr_count": 12,
        #     "start_offset": 8,
        #     "bit_offset": 3,
        #     "ocr_weights":"C:/Users/pc/Desktop/CODE_BASE/vasline_latest_codes/Models/code_on_cap_best.pt",
        #     "product_id":"44",
        #     "reference_image":"C:/Users/pc/Desktop/SKU_Images/Europe_100ml_line_1.jpg",
        #     "sku_id":"Europe_100ml"},  # Srilanka


    }


    if sku in ocr_configs_line_1:
        save_ocr_config(ocr_configs_line_1[sku])
        print(f"OCR Configuration updated for SKU {sku}")
        return True
    else:
        print(f"No OCR configuration defined for SKU {sku}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            sku_number = int(sys.argv[1])
            update_ocr_config(sku_number)
        except ValueError:
            print("Invalid SKU number. Please provide a valid integer.")
    else:
        print("Please provide an SKU number as an argument.")
