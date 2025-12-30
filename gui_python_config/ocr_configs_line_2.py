import json
import sys
import os

ROOT_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

def rel_path(*paths):
    return os.path.join(ROOT_DIR, *paths)

def save_ocr_config(config):
    config_path = rel_path("gui_python_config", "Line_2_Code_Config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)  

    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)

        
def update_ocr_config(sku):
    sku = int(sku)

    ocr_configs_line_2 = {
        1: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_50ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_singapore_50_ml.Config"), 

            "camera_serial_number": "054121020057",
            "default_conf": 0.5,
            "iou_thersh": 0.75,
            "height_threshold":270,
            "ocr_count": 7,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 5,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_cap_best.pt"),
            "product_id":"41",
            "sku_id":"NEA_Hongkong_50gm"},  # NEA Hongkong 50ml
        

        2: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_50ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_singapore_50_ml.Config"), 

            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 13,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 5,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_sticker_16_july_best.pt"),
            "product_id":"40",
            "sku_id":"NEA_Korea_50ml"},  # NEA Korea 50ml


        3: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_50ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_singapore_50_ml.Config"), 

            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 5,
            "ocr_weights": rel_path("vaseline_line_2","Models","code_on_cap_best.pt"),
            "product_id":"47",
            "sku_id":"Singapore_50ml"},  # Singapore 50ml

        4: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_50ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_japan_40gm.Config"), 
            "camera_serial_number": "054121020057",
            "height_threshold":1095,
            "default_conf": 0.2, 
            "iou_thersh": 0.75,
            "ocr_count": 6,
             "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 5,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_bottom_best.pt"),
            "product_id":"46",
            "sku_id":"Japan_40gm"},  # japan 40gm

        5: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_50ml.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_singapore_50_ml.Config"), 

            "camera_serial_number": "054121020057",
            "height_threshold":270,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 6,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 5,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_cap_best.pt"),
            "product_id":"45",
            "sku_id":"Europe_50ml"},  # Europe 50ml


        6: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_10ml__23_12_25.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_Japan_80gm.Config"), 

            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 13,
            "start_offset": 0,
            "bit_offset": 5,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 4,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_sticker_16_july_best.pt"),
            "product_id":"39",
            "sku_id":"NEA_Korea_100ml"}, # NEA Korea 100ml

        7: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_10ml__23_12_25.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_Japan_80gm.Config"), 

            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 4,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_cap_best.pt"),
            "product_id":"44",
            "sku_id":"NEA_Korea_100ml"}, # NEA Hongkong 100ml
        
        8: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_10ml__23_12_25.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_Japan_80gm.Config"), 

            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 12,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 4,  
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_cap_best.pt"),
            "product_id":"35",
            "sku_id":"NEA_Korea_100ml"} , # Singapore 100ml

        9: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_10ml__23_12_25.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_Japan_80gm.Config"),
            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.2, 
            "iou_thersh": 0.75,
            "ocr_count": 7,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 4,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_bottom_best.pt"),
            "product_id":"38",
            "sku_id":"NEA_Korea_100ml"}, # Japan 80gm
        
        10: {"camera_config_After_filling": rel_path("vaseline_line_2","Config_Files","Line_2_After_filling","line_2_af_10ml__23_12_25.Config"),
            
            "camera_config_before_filling":rel_path("vaseline_line_2","Config_Files","Line_2_before_filling","line-2_50_ml all sku's.Config"),

            "camera_config_ocr":rel_path("vaseline_line_2","Config_Files","Line_2_OCR","line_2_Japan_80gm.Config"),

            "camera_serial_number": "054121020057",
            "height_threshold":1680,
            "default_conf": 0.5, 
            "iou_thersh": 0.75,
            "ocr_count": 8,
            "start_offset": 1,
            "bit_offset": 3,
            "recipe_start_offset": 0,
            "recipe_bit_offset": 4,
            "ocr_weights":rel_path("vaseline_line_2","Models","code_on_cap_best.pt"),
            "product_id":"44",
            "sku_id":"NEA_Korea_100ml"}  # Europe 100ml


        

    }


    if sku in ocr_configs_line_2:
        save_ocr_config(ocr_configs_line_2[sku])
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

