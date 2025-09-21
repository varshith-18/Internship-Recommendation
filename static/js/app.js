// static/js/app.js

// Utility: show one screen at a time
function showScreen(id) {
  document.querySelectorAll('.container section').forEach(sec => sec.classList.add('d-none'));
  document.getElementById(id).classList.remove('d-none');
}

// ----------------
// 1. Welcome Screen → Eligibility
// ----------------
document.getElementById('start-btn').addEventListener('click', () => {
  showScreen('eligibility-screen');
});

// ----------------
// 2. Eligibility Check
// ----------------
let eligibility = { age: null, income: null, institution: false };

// Age buttons
document.querySelectorAll('#eligibility-screen [data-age]').forEach(btn => {
  btn.addEventListener('click', () => {
    eligibility.age = btn.dataset.age;

    // Highlight selection
    document.querySelectorAll('#eligibility-screen [data-age]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// Income buttons
document.querySelectorAll('#eligibility-screen [data-income]').forEach(btn => {
  btn.addEventListener('click', () => {
    eligibility.income = btn.dataset.income;

    // Highlight selection
    document.querySelectorAll('#eligibility-screen [data-income]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// Institution checkbox
document.getElementById('institution-check').addEventListener('change', e => {
  eligibility.institution = e.target.checked;
});

// Check eligibility
document.getElementById('check-eligibility').addEventListener('click', () => {
  const ok = eligibility.age === '21-24' && eligibility.income === 'lt8' && eligibility.institution;

  if (ok) {
    showScreen('profile-screen');
  } else {
    showScreen('ineligible-screen');
  }
});

// ----------------
// 3. Profile Input
// ----------------
let profile = {
  education: null,
  skills: [],
  sectors: [],
  location: ''
};

// Education buttons
document.querySelectorAll('#profile-screen .btn-education').forEach(btn => {
  btn.addEventListener('click', () => {
    profile.education = btn.textContent.trim();

    // Highlight selection
    document.querySelectorAll('#profile-screen .btn-education').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// Skills & interests bubbles (toggle)
document.querySelectorAll('#profile-screen .bubble').forEach(btn => {
  btn.addEventListener('click', () => {
    const value = btn.textContent.trim();

    if (btn.classList.contains('selected')) {
      btn.classList.remove('selected');
      profile.skills = profile.skills.filter(s => s !== value);
      profile.sectors = profile.sectors.filter(s => s !== value);
    } else {
      btn.classList.add('selected');
      // If emoji or predefined sector → sectors, else → skills
      if (/[\u{1F300}-\u{1FAFF}]/u.test(value)) {
        profile.sectors.push(value);
      } else {
        profile.skills.push(value);
      }
    }
  });
});

// Location input
document.getElementById('location').addEventListener('input', e => {
  profile.location = e.target.value.trim();
});

// ----------------
// 4. Fetch Recommendations
// ----------------
document.getElementById('find-btn').addEventListener('click', async () => {
  if (!profile.education) {
    alert('Please select your education.');
    return;
  }

  const payload = {
    education: profile.education,
    skills: profile.skills.join(','),
    sectors: profile.sectors.join(','),
    location: profile.location
  };

  const res = await fetch('/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const results = await res.json();
  const container = document.getElementById('results');
  container.innerHTML = '';

  if (!results || results.length === 0) {
    container.innerHTML = '<div class="alert alert-info">No matches found.</div>';
  } else {
    results.forEach(r => {
      const card = document.createElement('div');
      card.className = 'card mb-2';
      card.innerHTML = `
        <div class="card-body">
          <h5 class="card-title">${r.title} <small class="text-muted">(${r.sector})</small></h5>
          <p class="mb-1"><strong>Location:</strong> ${r.location}</p>
          <p class="mb-1"><strong>Skills Required:</strong> ${r.skills_required}</p>
          <p class="mb-1"><strong>Matched Skills:</strong> ${r.matched_skills.join(', ')}</p>
          <p class="mb-1"><strong>Score:</strong> ${r.score}</p>
          <p class="mb-0">${r.description || ''}</p>
        </div>`;
      container.appendChild(card);
    });
  }

  showScreen('results-screen');
});
