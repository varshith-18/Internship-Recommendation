// static/js/app.js
document.getElementById('profileForm').addEventListener('submit', async function (e) {
e.preventDefault();
const education = document.getElementById('education').value;
const skills = document.getElementById('skills').value;
const sectors = document.getElementById('sectors').value;
const location = document.getElementById('location').value;


const payload = { education, skills, sectors, location };
const res = await fetch('/recommend', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(payload)
});


const data = await res.json();
const results = data.results || [];
const container = document.getElementById('results');
container.innerHTML = '';


if (results.length === 0) {
container.innerHTML = '<div class="alert alert-info">No matches found.</div>';
return;
}


results.forEach(r => {
const card = document.createElement('div');
card.className = 'card mb-2';
card.innerHTML = `
<div class="card-body">
<h5 class="card-title">${r.title} <small class="text-muted">(${r.sector})</small></h5>
<p class="mb-1"><strong>Location:</strong> ${r.location}</p>
<p class="mb-1"><strong>Matched skills:</strong> ${r.matched_skills.join(', ') || 'None'}</p>
<p class="mb-1"><strong>Score:</strong> ${r.score}</p>
<p class="mb-0">${r.description || ''}</p>
</div>
`;
container.appendChild(card);
});
});