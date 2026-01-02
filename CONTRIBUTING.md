# 🤝 Contributing to Legal Summarizer

Thanks for your interest in contributing to Legal Summarizer! 🚀

We're building an AI-powered document summarization platform to:
- ⚖️ Simplify complex legal documents
- 🚀 Help startups understand contracts faster
- 🔍 Identify key risks and obligations
- 📊 Empower entrepreneurs with legal insights

---

## 📌 How to Contribute

### 1️⃣ Fork & Clone the Repository

Fork the repository and clone it locally:

```bash
git clone https://github.com/your-username/Legal-Summarizer.git
cd Legal-Summarizer
```

---

### 2️⃣ Create a New Branch

Use a clear and descriptive branch name:

```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/add-comparison` - New feature
- `bugfix/fix-upload-issue` - Bug fix
- `docs/update-readme` - Documentation
- `perf/optimize-summarizer` - Performance improvement

---

### 3️⃣ Make Your Changes

You can help by:

💻 **AI & NLP Features**
- Improve summarization accuracy
- Add new NLP models or fine-tuning
- Implement document comparison
- Add risk assessment features

🐞 **Bug Fixes & Performance**
- Fix bugs or improve performance
- Optimize document processing speed
- Reduce API response times
- Improve memory efficiency

🎨 **Frontend & UI/UX**
- Improve user interface design
- Enhance accessibility features
- Add dark mode support
- Improve mobile responsiveness

🔐 **Security & Backend**
- Enhance security features
- Optimize database queries
- Improve error handling
- Add input validation

📚 **Documentation & Testing**
- Improve documentation clarity
- Add code examples
- Write unit tests
- Add integration tests

🌐 **Localization**
- Add multilingual support
- Translate UI elements
- Support multiple languages in summarization

**Ensure your changes:**
- ✅ Align with Legal Summarizer's goals
- ✅ Are clean and well-structured
- ✅ Include proper error handling
- ✅ Have clear comments for complex logic

---

### 4️⃣ Test Before You Commit

**Backend Testing:**

```bash
# Activate virtual environment
cd fastapi_agents
source venv/bin/activate

# Run tests
pytest

# Run specific test
pytest tests/test_summarizer.py

# Check with coverage
pytest --cov=services tests/
```

**Frontend Testing:**

```bash
# Navigate to frontend
cd front

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

**Manual Testing:**

- [ ] Run backend locally (`python main.py`)
- [ ] Run frontend locally (`npm run dev`)
- [ ] Test document upload functionality
- [ ] Verify summarization accuracy
- [ ] Check UI responsiveness
- [ ] Test error handling with invalid inputs
- [ ] Verify database operations work correctly

**Testing Checklist:**

- [ ] All tests pass
- [ ] No console errors
- [ ] No security vulnerabilities
- [ ] Code follows style guide
- [ ] Performance is acceptable

---

### 5️⃣ Commit and Push

Write clear, descriptive commit messages following this format:

```bash
git add .
git commit -m "type: short description of your change

- Additional detail about the change
- Another detail if needed
- Related issue #123"

git push origin feature/your-feature-name
```

**Commit message types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `perf:` - Performance improvements
- `test:` - Test additions/updates
- `refactor:` - Code refactoring

**Example:**

```bash
git commit -m "feat: add document comparison feature

- Implement side-by-side comparison view
- Add highlighting for differences
- Include export to PDF functionality
- Add tests for comparison logic

Closes #42"
```

---

### 6️⃣ Submit a Pull Request (PR)

Go to your fork on GitHub and click **Compare & Pull Request**

**In your PR description, include:**

1. **What changed?**
   - Clear description of your changes
   - Why you made these changes

2. **Type of Change**
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Performance improvement
   - [ ] Documentation update
   - [ ] Security improvement

3. **Related Issues**
   - Link to related GitHub issues
   - Example: "Closes #123" or "Fixes #456"

4. **Testing Done**
   - Describe how you tested your changes
   - Include test results
   - List test cases covered

5. **Screenshots (if applicable)**
   - Before/after screenshots for UI changes
   - Demo GIFs for new features
   - Error handling examples

6. **Checklist**
   - [ ] My code follows the style guidelines
   - [ ] I have tested my changes locally
   - [ ] I have updated documentation
   - [ ] I have added comments for complex code
   - [ ] All tests pass
   - [ ] No new warnings generated
   - [ ] I have linked related issues

**Example PR Description:**

```markdown
## What Changed?
Added a new document comparison feature that allows users to compare two legal documents side-by-side.

## Why?
Users requested the ability to compare different versions of contracts to identify changes and differences.

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Documentation update

## How to Test?
1. Upload two legal documents
2. Click the "Compare Documents" button
3. View differences highlighted in real-time
4. Export comparison as PDF

## Screenshots
[Screenshot showing the comparison view]

## Related Issues
Closes #78
Related to #45

## Testing
- [x] Tested with PDF files
- [x] Tested with DOCX files
- [x] Tested with TXT files
- [x] Added unit tests for comparison logic
- [x] All tests pass ✅
```

---

## ✅ Contribution Checklist

Before submitting your PR, verify:

### Code Quality
- [ ] Code follows project style guide
- [ ] Variable names are descriptive
- [ ] Complex logic has comments
- [ ] No hardcoded values
- [ ] No debugging code left in

### Testing
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] No test failures introduced
- [ ] Code coverage maintained or improved

### Documentation
- [ ] README.md updated (if needed)
- [ ] Code comments added where needed
- [ ] Docstrings added for functions
- [ ] API changes documented
- [ ] New dependencies documented

### Security
- [ ] No hardcoded secrets or API keys
- [ ] Input validation implemented
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No CORS issues

### Performance
- [ ] No unnecessary loops
- [ ] No unoptimized database queries
- [ ] No memory leaks
- [ ] Response times acceptable
- [ ] Large files handled efficiently

### Git
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] Commits are clean and descriptive
- [ ] No unnecessary files committed
- [ ] .gitignore respected

---

## 📋 Contribution Types & Effort

| Type | Time | Difficulty | Impact |
|------|------|-----------|--------|
| Report bug | 5 min | ⭐ Easy | Medium |
| Suggest feature | 5 min | ⭐ Easy | Medium |
| Fix typo | 10 min | ⭐ Easy | Low |
| Update docs | 15 min | ⭐ Easy | Medium |
| Write tests | 30 min | ⭐⭐ Medium | High |
| Fix small bug | 1 hour | ⭐⭐ Medium | High |
| Add small feature | 2 hours | ⭐⭐ Medium | High |
| Add big feature | 5+ hours | ⭐⭐⭐ Hard | Very High |
| Optimize performance | 3 hours | ⭐⭐⭐ Hard | Very High |

---

## 🔧 Development Setup

### Prerequisites

```bash
# Required
- Git
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ or MySQL 5.7+
- Docker & Docker Compose (optional)
```

### Quick Setup

**Backend:**
```bash
cd fastapi_agents
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd front
npm install
npm run dev
```

**Database (Docker):**
```bash
docker run --name legal-db \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:14
```

---

## 💬 Need Help?

If you have questions or suggestions:

**Open an Issue:** [GitHub Issues](https://github.com/Gov-10/capstone-proj/issues)
- Report bugs
- Suggest features
- Ask questions
- Discuss improvements


---



---

## 🎯 PR Review Process

### What Happens After You Submit?

1. **Automated Checks Run** (5-10 min)
   - Tests must pass ✅
   - Code style checked
   - Security scan runs

2. **Code Review** (24-48 hours)
   - Maintainers review your code
   - They may request changes
   - They may ask questions

3. **Your Response** (24 hours)
   - Make requested changes
   - Commit to same branch
   - Push updates
   - PR updates automatically

4. **Approval & Merge** (1-2 days)
   - Once approved, maintainer merges
   - Your code goes live! 🎉
   - You get recognition

---

## 🌟 Recognition

All contributors get:
- ✨ Credit in project README
- 📊 Visible on GitHub contributors page
- 🎯 Portfolio experience
- 👥 Community recognition
- 🚀 Impact on real projects


---

## ⚡ Quick Contribution Checklist

- [ ] Fork the repository
- [ ] Create a branch (`feature/my-feature`)
- [ ] Make changes in your editor
- [ ] Test locally (run tests)
- [ ] Commit with clear message
- [ ] Push to your fork
- [ ] Create Pull Request on GitHub
- [ ] Respond to feedback
- [ ] Celebrate when merged! 🎉

---

<div align="center">

### 🎉 Thank You for Contributing!

**Your contributions make Legal Summarizer better for everyone.**

Every PR, bug report, and suggestion matters.

---

### Ready to Contribute?

1. **Pick what interests you** - Bug fix? Feature? Docs?
2. **Fork & clone** the repository
3. **Make your changes** with clear commits
4. **Test everything** before submitting
5. **Submit a PR** with a good description
6. **Wait for feedback** and respond promptly


---

**Happy Contributing! 🚀💚**

</div>