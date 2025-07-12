# Flask API Practical Exercise - Submission

**Exercise**: Flask-based API with MVC Architecture for Prompt Matching  
**Status**: ✅ **FULLY COMPLETED**

## 🎯 Requirements Fulfilled

✅ Flask API with MVC architecture (Service + View layers)  
✅ POST endpoint with JSON input structure  
✅ All 5 prompt matching rules implemented  
✅ "Missing Data" and "Invalid Prompt" error handling  
✅ Edge case handling and robust validation  

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python app.py
```

**Test API:**
```bash
python test_api.py
```

## 📊 Results

**✅ ALL TESTS PASSED** - 17/17 test scenarios successful:
- 5/5 Valid prompt matches
- 6/6 Missing data scenarios  
- 4/4 Invalid prompt scenarios
- 2/2 Edge cases

## 🏗️ Architecture

- **Service Layer**: `services/prompt_service.py` - Business logic
- **View Layer**: `views/prompt_controller.py` - Request handling  
- **Main App**: `app.py` - Flask application and routing

## 📋 Prompt Mapping

| Prompt | Situation | Level | File Type |
|---------|-----------|-------|-----------|
| Prompt 1 | Commercial Auto | Structure | Summary Report |
| Prompt 2 | General Liability | Summarize | Deposition |
| Prompt 3 | Commercial Auto | Summarize | Summons |
| Prompt 4 | Workers Compensation | Structure | Medical Records |
| Prompt 5 | Workers Compensation | Summarize | Summons |

**Ready for production deployment** 🚀 