# 🤝 Contributing to Collectorium

Collectorium'a katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, katkı sürecini kolaylaştırmak için hazırlanmıştır.

## 📋 Code of Conduct

- Saygılı ve yapıcı olun
- Farklı görüşlere açık olun
- Profesyonel bir dil kullanın
- Topluluğu destekleyin

## 🚀 Hızlı Başlangıç

### 1. Fork & Clone

```bash
# Fork edin (GitHub web interface)
# Clone yapın
git clone https://github.com/YOUR_USERNAME/collectorium.git
cd collectorium
```

### 2. Development Environment

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -e ".[dev,test,lint]"

# Pre-commit hooks
pre-commit install
```

### 3. Branch Oluştur

```bash
git checkout -b feature/your-feature-name
# veya
git checkout -b fix/bug-description
```

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: Yeni özellik
- **fix**: Bug fix
- **docs**: Dokümantasyon
- **style**: Formatting, eksik semicolons, vb.
- **refactor**: Code refactoring
- **test**: Test ekleme/düzenleme
- **chore**: Build, dependency güncellemeleri

### Örnekler

```bash
feat(listings): add image upload support
fix(cart): resolve quantity update bug
docs(readme): update installation instructions
test(orders): add checkout flow tests
```

## 🧪 Testing

Pull request göndermeden önce testlerin geçtiğinden emin olun:

```bash
# Tüm testler
pytest

# Coverage
pytest --cov=. --cov-report=html

# Linting
make lint

# Formatting
make format
```

## 📦 Pull Request Process

### 1. Checklist

- [ ] Kod değişiklikleri test edildi
- [ ] Yeni özellikler için testler yazıldı
- [ ] Dokümantasyon güncellendi
- [ ] Commit mesajları kurallara uygun
- [ ] Linting hataları yok
- [ ] Pre-commit hooks geçti

### 2. PR Description Template

```markdown
## 🎯 Amaç
Bu PR ne yapar?

## 🔧 Değişiklikler
- Değişiklik 1
- Değişiklik 2

## 🧪 Test Edilen Senaryolar
- [ ] Senaryo 1
- [ ] Senaryo 2

## 📸 Screenshots (eğer UI değişikliği varsa)
Ekran görüntüleri ekleyin

## 📝 Notlar
Ek bilgiler
```

### 3. Review Process

- Maintainer'lar PR'ınızı inceleyecek
- Değişiklik talepleri olabilir
- En az 1 approval gerekli
- CI/CD checks geçmeli

## 🏗️ Development Workflow

### 1. Issue Oluştur

Büyük değişiklikler için önce issue açın:

```markdown
**Problem**: Ne sorunu çözüyor?
**Önerilen Çözüm**: Nasıl çözülecek?
**Alternatifler**: Başka seçenekler var mı?
```

### 2. Feature Development

```bash
# Güncel main branch
git checkout main
git pull upstream main

# Yeni feature branch
git checkout -b feature/awesome-feature

# Kod yazın, commit edin
git add .
git commit -m "feat(module): add awesome feature"

# Push
git push origin feature/awesome-feature
```

### 3. Bug Fixes

```bash
# Bug fix branch
git checkout -b fix/issue-123-cart-bug

# Fix, test, commit
git commit -m "fix(cart): resolve quantity calculation bug"
```

## 🎨 Code Style

### Python

- **Black** için formatting (88 char line length)
- **Ruff** için linting
- **isort** için import sorting
- Type hints kullanın (Python 3.11+)

```python
from typing import Optional

def calculate_total(price: Decimal, quantity: int) -> Decimal:
    """Calculate total price."""
    return price * quantity
```

### Django

- Class-based views (CBVs) tercih edin
- Model'lerde `__str__` tanımlayın
- Docstrings yazın
- QuerySet optimizasyonu (`select_related`, `prefetch_related`)

### Templates

- TailwindCSS kullanın
- Alpine.js için minimal JavaScript
- Accessibility (a11y) dikkat edin

## 📖 Documentation

### Docstrings

```python
def create_listing(user, data):
    """
    Create a new listing for a seller.
    
    Args:
        user (User): The seller creating the listing
        data (dict): Listing data (title, price, etc.)
        
    Returns:
        Listing: The created listing instance
        
    Raises:
        PermissionError: If user is not a seller
        ValidationError: If data is invalid
    """
    pass
```

### README Updates

Yeni özellikler için README'yi güncelleyin:

```markdown
## 🆕 Yeni Özellik Adı

Özellik açıklaması

### Kullanım

\`\`\`python
# Kod örneği
\`\`\`
```

## 🐛 Bug Reports

### Template

```markdown
**Bug Açıklaması**
Kısa ve net bir açıklama

**Reproduce Steps**
1. Adım 1
2. Adım 2
3. Hata görülür

**Beklenen Davranış**
Ne olması gerekiyordu?

**Screenshots**
Varsa ekleyin

**Environment**
- OS: [örn. Windows 10]
- Python: [örn. 3.11.0]
- Django: [örn. 5.2]
```

## 💡 Feature Requests

### Template

```markdown
**Özellik Açıklaması**
Ne istersiniz?

**Problem**
Hangi problemi çözüyor?

**Önerilen Çözüm**
Nasıl implement edilmeli?

**Alternatifler**
Başka yaklaşımlar?
```

## 🏆 Recognition

Katkıda bulunanlar:

- README'de Contributors bölümüne eklenirsiniz
- GitHub Insights'ta görünürsünüz
- Özel teşekkür notları alırsınız

## 📞 İletişim

- **GitHub Issues**: Bug reports & feature requests
- **Discussions**: Sorular ve tartışmalar
- **Email**: dev@collectorium.com

---

**Teşekkürler! 🙏**

Katkılarınız Collectorium'u daha iyi hale getiriyor.

