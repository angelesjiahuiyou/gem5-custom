# Step 3
python cpt_step3_relative.py step2/parsed_stats_int_sc-imec-a15-p4_sram-only_typical.csv step2/parsed_stats_int_sc-imec-a15-p4_stt-l2_typical.csv step2/parsed_stats_int_sc-imec-a15-p4_stt-l2_worst.csv step2/parsed_stats_int_sc-imec-a15-p4_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_int_sc-imec-a15-p2_sram-only_typical.csv step2/parsed_stats_int_sc-imec-a15-p2_stt-l2_typical.csv step2/parsed_stats_int_sc-imec-a15-p2_stt-l2_worst.csv step2/parsed_stats_int_sc-imec-a15-p2_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_int_sc-imec-a15-p0_sram-only_typical.csv step2/parsed_stats_int_sc-imec-a15-p0_stt-l2_typical.csv step2/parsed_stats_int_sc-imec-a15-p0_stt-l2_worst.csv step2/parsed_stats_int_sc-imec-a15-p0_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_int_sc-i7-6700_sram-only_typical.csv step2/parsed_stats_int_sc-i7-6700_stt-l3_typical.csv step2/parsed_stats_int_sc-i7-6700_stt-l3_worst.csv step2/parsed_stats_int_sc-i7-6700_stt-l3_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_int_sc-a53-odn2_sram-only_typical.csv step2/parsed_stats_int_sc-a53-odn2_stt-l2_typical.csv step2/parsed_stats_int_sc-a53-odn2_stt-l2_worst.csv step2/parsed_stats_int_sc-a53-odn2_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_fp_sc-imec-a15-p4_sram-only_typical.csv step2/parsed_stats_fp_sc-imec-a15-p4_stt-l2_typical.csv step2/parsed_stats_fp_sc-imec-a15-p4_stt-l2_worst.csv step2/parsed_stats_fp_sc-imec-a15-p4_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_fp_sc-imec-a15-p2_sram-only_typical.csv step2/parsed_stats_fp_sc-imec-a15-p2_stt-l2_typical.csv step2/parsed_stats_fp_sc-imec-a15-p2_stt-l2_worst.csv step2/parsed_stats_fp_sc-imec-a15-p2_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_fp_sc-imec-a15-p0_sram-only_typical.csv step2/parsed_stats_fp_sc-imec-a15-p0_stt-l2_typical.csv step2/parsed_stats_fp_sc-imec-a15-p0_stt-l2_worst.csv step2/parsed_stats_fp_sc-imec-a15-p0_stt-l2_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_fp_sc-i7-6700_sram-only_typical.csv step2/parsed_stats_fp_sc-i7-6700_stt-l3_typical.csv step2/parsed_stats_fp_sc-i7-6700_stt-l3_worst.csv step2/parsed_stats_fp_sc-i7-6700_stt-l3_w-write.csv
python cpt_step3_relative.py step2/parsed_stats_fp_sc-a53-odn2_sram-only_typical.csv step2/parsed_stats_fp_sc-a53-odn2_stt-l2_typical.csv step2/parsed_stats_fp_sc-a53-odn2_stt-l2_worst.csv step2/parsed_stats_fp_sc-a53-odn2_stt-l2_w-write.csv

# Step 4
python cpt_step4_standardization.py step3/*

# Step 5
python cpt_step5_pca.py step4/*

# Step 6
python cpt_step6_regression.py step4/slowdown_*
