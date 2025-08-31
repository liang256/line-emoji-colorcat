# Refactoring Plan

## Current Architecture Issues
1. **subprocess dependency** - run_pipeline.py uses subprocess to call other scripts, inefficient and poor error handling
2. **Code duplication** - hex_to_rgb implemented in multiple places
3. **Scattered config parsing** - color parsing logic repeated across modules
4. **No unified API** - lack of common interface design
5. **Temp file management** - manual cleanup of intermediate files required

## Refactoring Steps
1. Create shared `utils.py` for:
   - Color conversion functions (hex_to_rgb, rgb_to_hex)
   - Config file parsing
   - Common data structures/dataclasses

2. Convert modules to importable functions:
   - `find_fill_area.py` → `find_fill_area(input_path, **kwargs) -> mask_array`
   - `composite.py` → `composite(lineart_path, mask, fill_color) -> result_array`

3. Redesign pipeline as pure Python:
   - Remove subprocess calls
   - Use in-memory arrays instead of temp files
   - Add proper logging and error handling

4. Create unified config system:
   - Use dataclass for ColorConfig
   - Support multiple color formats (hex, rgb, named colors)

5. Add type hints and proper documentation

## Implementation Priority
1. utils.py with common functions
2. Refactor core modules to return arrays
3. Update run_pipeline.py to use imports
4. Add comprehensive error handling
5. Performance optimization