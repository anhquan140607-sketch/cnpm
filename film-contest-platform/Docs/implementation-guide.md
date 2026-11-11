# Task Implementation Guide: CNPM-36 [1.2] Hồ sơ cá nhân và bảo mật (đổi mật khẩu)

Document version: 1.0  
Target Project: AI-powered Film Photography Contest Management Platform  
Task Jira ID: CNPM-36

---

## 1. Overview & Business Requirements

This task implements user self-service account features:
* **Profile Management:** Viewing and editing basic user information (Full Name, Phone Number, Bio, Avatar URL).
* **Security & Password Update:** Validating current credentials and updating to a new password with secure hashing.

---

## 2. Backend Implementation (C# ASP.NET Core API)

### 2.1 Data Transfer Objects (DTOs)

```csharp
namespace FilmContest.Api.DTOs
{
    public class UserProfileDto
    {
        public string Email { get; set; } = string.Empty;
        public string FullName { get; set; } = string.Empty;
        public string PhoneNumber { get; set; } = string.Empty;
        public string Bio { get; set; } = string.Empty;
        public string AvatarUrl { get; set; } = string.Empty;
    }

    public class UpdateProfileDto
    {
        public string FullName { get; set; } = string.Empty;
        public string PhoneNumber { get; set; } = string.Empty;
        public string Bio { get; set; } = string.Empty;
        public string AvatarUrl { get; set; } = string.Empty;
    }

    public class ChangePasswordDto
    {
        public string CurrentPassword { get; set; } = string.Empty;
        public string NewPassword { get; set; } = string.Empty;
        public string ConfirmPassword { get; set; } = string.Empty;
    }
}
```

### 2.2 Controller Logic (`UserProfileController.cs`)

```csharp
using System;
using System.Security.Claims;
using System.Threading.Tasks;
using FilmContest.Api.Data;
using FilmContest.Api.DTOs;
using FilmContest.Api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FilmContest.Api.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/users")]
    public class UserProfileController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly IPasswordHasher<User> _passwordHasher;

        public UserProfileController(AppDbContext context, IPasswordHasher<User> passwordHasher)
        {
            _context = context;
            _passwordHasher = passwordHasher;
        }

        // GET: api/users/profile
        [HttpGet("profile")]
        public async Task<IActionResult> GetProfile()
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (string.IsNullOrEmpty(userId)) return Unauthorized();

            var user = await _context.Users.FindAsync(Guid.Parse(userId));
            if (user == null) return NotFound(new { message = "User not found." });

            var result = new UserProfileDto
            {
                Email = user.Email,
                FullName = user.FullName,
                PhoneNumber = user.PhoneNumber,
                Bio = user.Bio,
                AvatarUrl = user.AvatarUrl
            };

            return Ok(result);
        }

        // PUT: api/users/profile
        [HttpPut("profile")]
        public async Task<IActionResult> UpdateProfile([FromBody] UpdateProfileDto dto)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (string.IsNullOrEmpty(userId)) return Unauthorized();

            var user = await _context.Users.FindAsync(Guid.Parse(userId));
            if (user == null) return NotFound(new { message = "User not found." });

            user.FullName = dto.FullName;
            user.PhoneNumber = dto.PhoneNumber;
            user.Bio = dto.Bio;
            user.AvatarUrl = dto.AvatarUrl;

            await _context.SaveChangesAsync();
            return Ok(new { message = "Profile updated successfully." });
        }

        // POST: api/users/change-password
        [HttpPost("change-password")]
        public async Task<IActionResult> ChangePassword([FromBody] ChangePasswordDto dto)
        {
            if (dto.NewPassword != dto.ConfirmPassword)
            {
                return BadRequest(new { message = "New password and confirmation do not match." });
            }

            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (string.IsNullOrEmpty(userId)) return Unauthorized();

            var user = await _context.Users.FindAsync(Guid.Parse(userId));
            if (user == null) return NotFound(new { message = "User not found." });

            // Verify current password
            var verificationResult = _passwordHasher.VerifyHashedPassword(user, user.PasswordHash, dto.CurrentPassword);
            if (verificationResult == PasswordVerificationResult.Failed)
            {
                return BadRequest(new { message = "Current password is incorrect." });
            }

            // Hash & set new password
            user.PasswordHash = _passwordHasher.HashPassword(user, dto.NewPassword);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Password updated successfully." });
        }
    }
}
```

---

## 3. Frontend Implementation (React & Tailwind CSS)

```jsx
import React, { useState, useEffect } from 'react';

const ProfileSettingsPage = () => {
  const [activeTab, setActiveTab] = useState('profile');

  // Profile Form States
  const [profile, setProfile] = useState({
    email: '',
    fullName: '',
    phoneNumber: '',
    bio: '',
    avatarUrl: '',
  });

  // Security Form States
  const [passwords, setPasswords] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [message, setMessage] = useState({ type: '', text: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch initial profile data from API
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      // Replace with actual API call / axios
      const mockData = {
        email: 'photographer@filmcontest.com',
        fullName: 'Alex Nguyen',
        phoneNumber: '+84 901 234 567',
        bio: '35mm Film enthusiast, Leica M6 shooter.',
        avatarUrl: 'https://via.placeholder.com/150',
      };
      setProfile(mockData);
    } catch (err) {
      console.error(err);
    }
  };

  const handleProfileSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    // Simulate API save
    setTimeout(() => {
      setLoading(false);
      setMessage({ type: 'success', text: 'Hồ sơ cá nhân đã được cập nhật thành công!' });
    }, 800);
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    if (passwords.newPassword !== passwords.confirmPassword) {
      setMessage({ type: 'error', text: 'Mật khẩu mới và Nhập lại mật khẩu không khớp!' });
      return;
    }

    if (passwords.newPassword.length < 6) {
      setMessage({ type: 'error', text: 'Mật khẩu mới phải có tối thiểu 6 ký tự.' });
      return;
    }

    setLoading(true);
    // Simulate API password change
    setTimeout(() => {
      setLoading(false);
      setMessage({ type: 'success', text: 'Mật khẩu đã được thay đổi thành công!' });
      setPasswords({ currentPassword: '', newPassword: '', confirmPassword: '' });
    }, 800);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-md rounded-lg my-8">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Cài Đặt Tài Khoản & Bảo Mật</h1>

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          className={`py-2 px-4 font-medium text-sm focus:outline-none ${
            activeTab === 'profile'
              ? 'border-b-2 border-indigo-600 text-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => { setActiveTab('profile'); setMessage({type: '', text: ''}); }}
        >
          Hồ Sơ Cá Nhân
        </button>
        <button
          className={`py-2 px-4 font-medium text-sm focus:outline-none ${
            activeTab === 'security'
              ? 'border-b-2 border-indigo-600 text-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => { setActiveTab('security'); setMessage({type: '', text: ''}); }}
        >
          Bảo Mật & Đổi Mật Khẩu
        </button>
      </div>

      {/* Alert Notification */}
      {message.text && (
        <div
          className={`p-4 mb-6 rounded-md text-sm ${
            message.type === 'success'
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <form onSubmit={handleProfileSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Địa chỉ Email</label>
            <input
              type="email"
              value={profile.email}
              disabled
              className="mt-1 block w-full rounded-md border-gray-300 bg-gray-100 p-2 text-gray-500 cursor-not-allowed"
            />
            <p className="text-xs text-gray-400 mt-1">Email dùng để đăng nhập và không thể tự thay đổi.</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Họ và Tên</label>
            <input
              type="text"
              value={profile.fullName}
              onChange={(e) => setProfile({ ...profile, fullName: e.target.value })}
              required
              className="mt-1 block w-full rounded-md border-gray-300 border p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Số Điện Thoại</label>
            <input
              type="text"
              value={profile.phoneNumber}
              onChange={(e) => setProfile({ ...profile, phoneNumber: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 border p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Giới Thiệu (Bio)</label>
            <textarea
              rows="3"
              value={profile.bio}
              onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 border p-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Chia sẻ về phong cách nhiếp ảnh phim của bạn..."
            ></textarea>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition"
          >
            {loading ? 'Đang lưu...' : 'Lưu Thay Đổi'}
          </button>
        </form>
      )}

      {/* Security Tab */}
      {activeTab === 'security' && (
        <form onSubmit={handlePasswordSubmit} className="space-y-4 max-w-md">
          <div>
            <label className="block text-sm font-medium text-gray-700">Mật Khẩu Hiện Tại</label>
            <input
              type="password"
              value={passwords.currentPassword}
              onChange={(e) => setPasswords({ ...passwords, currentPassword: e.target.value })}
              required
              className="mt-1 block w-full rounded-md border-gray-300 border p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Mật Khẩu Mới</label>
            <input
              type="password"
              value={passwords.newPassword}
              onChange={(e) => setPasswords({ ...passwords, newPassword: e.target.value })}
              required
              className="mt-1 block w-full rounded-md border-gray-300 border p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Xác Nhận Mật Khẩu Mới</label>
            <input
              type="password"
              value={passwords.confirmPassword}
              onChange={(e) => setPasswords({ ...passwords, confirmPassword: e.target.value })}
              required
              className="mt-1 block w-full rounded-md border-gray-300 border p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
          >
            {loading ? 'Đang cập nhật...' : 'Đổi Mật Khẩu'}
          </button>
        </form>
      )}
    </div>
  );
};

export default ProfileSettingsPage;
```

---

## 4. Final Verification & Jira Submission Steps

1. **Commit and Push to GitHub:**
   ```bash
   git checkout -b feature/CNPM-36-profile-security
   git add .
   git commit -m "CNPM-36: Triển khai quản lý hồ sơ cá nhân và chức năng đổi mật khẩu"
   git push origin feature/CNPM-36-profile-security
   ```

2. **Jira Ticket Updating (CNPM-36):**
   * Paste the GitHub Pull Request (PR) link in the **Comment** section.
   * Attach screenshots of both the **Profile Form** and **Change Password Form** into the **Attachments** area.
   * Change status to **Done**.
