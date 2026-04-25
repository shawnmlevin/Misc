# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A personal collection of two standalone Python data-processing utilities. There is no build system, package manager, test suite, or CI/CD pipeline.

## Scripts

### `amazon_xray`
A Python script that parses an IMDb X-Ray JSON export and writes character appearance timelines to `xray.csv`. The input path is hardcoded as `/Users/{directory}/xray.json` and must be updated before use. Output columns: `nconst`, `character`, `start`, `end`.

- Uses Python 2-style CSV writing (`open(..., 'wb')`). If running on Python 3, change the file mode to `'w'` and add `newline=''`.
- Navigates a deeply nested JSON structure: `data['page']['sections']['left']['widgets']['widgetList'][0]['widgets']['widgetList'][1]['partitionedChangeList']`.

### `Convert_Wav_to_Data`
A Jupyter notebook (missing the `.ipynb` extension) that reads a stereo WAV file (`"16 The End.wav"`), randomly samples 2% of frames using a NumPy boolean mask, and writes the result to `theend.csv`. Both the input filename and output filename are hardcoded in the single code cell.

Dependencies: `pandas`, `numpy`, `scipy`

## Running the Scripts

```bash
# Run the X-Ray parser (update the path inside the file first)
python amazon_xray

# Open the notebook (rename or pass directly to Jupyter)
cp Convert_Wav_to_Data Convert_Wav_to_Data.ipynb
jupyter notebook Convert_Wav_to_Data.ipynb
```

## Git Branch

Active development branch: `claude/add-claude-documentation-CAp4D`
