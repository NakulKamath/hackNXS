import tempsessionInfo from "./sessionInfo.json" with { type : 'json' }
import tempdata from "./data.json" with { type : 'json' }

let sessionInfo = tempsessionInfo;
let data = tempdata;

const homePage = document.querySelector('.home-page');
const loginPage = document.querySelector('.login-page');
const signupPage = document.querySelector('.signup-page');
const dashboardPage = document.querySelector('.dashboard-page');
const aboutPage = document.querySelector('.about-page');
const contactPage = document.querySelector('.contact-page');
const profilePage = document.querySelector('.profile-page');
const additionalPage = document.querySelector('.signup-page-extra');

const announcer = document.querySelector('#announcer');

const nav_bar_home_btn = document.querySelector('#hisab');
const nav_bar_about_btn = document.querySelector('#about');
const nav_bar_dashboard_btn = document.querySelector('#dashboard');
const nav_bar_profile_btn = document.querySelector('#profile');
const nav_bar_contact_btn = document.querySelector('#contact');

const purpleBar = document.querySelector('#purple-bar');
const magentaBar = document.querySelector('#magenta-bar');
const blueBar = document.querySelector('#blue-bar');

const home_page_login_btn = document.querySelector('#login');
const home_page_signup_btn = document.querySelector('#signup');
const login_page_login_btn = document.querySelector('#user-login');
const signup_page_singup_btn = document.querySelector('#user-signup');
const profile_page_logout_btn = document.querySelector('#logout');
const about_page_start_btn = document.querySelector('#start');
const signup_page_complete_btn = document.querySelector('#user-complete');

let predictions;


console.log(localStorage);

function reloadLocal() {
    localStorage.sessionInfo = JSON.stringify(sessionInfo)
    localStorage.data = JSON.stringify(data)
    reloadData();
    console.log(localStorage);
}
function reloadData() {
    sessionInfo = JSON.parse(localStorage.sessionInfo);
    data = JSON.parse(localStorage.data);
}

if (localStorage.length === 0) {
    reloadLocal();
} else {
    reloadData();
}

launch();

function launch() {
    clearMain();
    if (sessionInfo.logged == false) {
        aboutPage.classList.remove('hidden');
    } else {
        profilePage.classList.remove('hidden');
        loadProfile();
    }
}

function clearMain() {
    homePage.classList.add('hidden');
    signupPage.classList.add('hidden');
    dashboardPage.classList.add('hidden');
    aboutPage.classList.add('hidden');
    contactPage.classList.add('hidden');
    profilePage.classList.add('hidden');
    loginPage.classList.add('hidden');
    additionalPage.classList.add('hidden');
}
async function loadPage() {
    purpleBar.classList.remove('hidden');
    await timer(100);
    magentaBar.classList.remove('hidden');
    await timer(100);
    blueBar.classList.remove('hidden');
    await timer(2000);
    purpleBar.classList.add('hidden');
    magentaBar.classList.add('hidden');
    blueBar.classList.add('hidden');
}
function loadProfile() {
    let name = document.querySelector('#name');
    let gender = document.querySelector('#gender');
    let since = document.querySelector('#since');
    let score = document.querySelector('#score');
    let age = document.querySelector('#age');
    let total = document.querySelector('#total');
    let month = document.querySelector('#month');
    let goal = document.querySelector('#goal');
    let progress = document.querySelector('.progress');

    let user = data.users[sessionInfo.currentUser];
    let progressValue = user.total / user.goal * 100

    name.textContent = user.information.first + " " + user.information.last;
    gender.textContent = user.information.gender;
    since.textContent = user.information.since;
    age.textContent = user.information.age;
    score.textContent = user.information.score;
    total.textContent = user.total;
    month.textContent = user.month;
    goal.textContent = user.goal;
    progress.style.width = progressValue + '%'
}

function loadDashboard() {
    let income = document.querySelector('#dashboard-income');
    let food = document.querySelector('#dashboard-food');
    let utilities = document.querySelector('#dashboard-utilities');
    let travel = document.querySelector('#dashboard-travel');
    let medicals = document.querySelector('#dashboard-medicals');
    let entertainment = document.querySelector('#dashboard-entertainment');
    let savings = document.querySelector('#dashboard-savings');
    let emergency = document.querySelector('#dashboard-emergency');
    let grocery = document.querySelector('#dashboard-grocery');

    let user = data.users[sessionInfo.currentUser];

    income.textContent = user.income;
    food.textContent = user.predictions.food;
    medicals.textContent = user.predictions.medicals;
    entertainment.textContent = user.predictions.entertainment;
    travel.textContent = user.predictions.travel;
    emergency.textContent = user.predictions.emergency;
    savings.textContent = user.predictions.savings;
    utilities.textContent = user.predictions.utilities;
    grocery.textContent = user.predictions.grocery;
}

about_page_start_btn.addEventListener('click', async() => {
    loadPage();
    await timer(300);
    if (sessionInfo.logged == false) {
        clearMain();
        homePage.classList.remove('hidden');
    } else {
        clearMain();
        profilePage.classList.remove('hidden');
        loadProfile();
    }
})

home_page_login_btn.addEventListener('click', async() => {
    loadPage();
    await timer(500);
    clearMain();
    loginPage.classList.remove('hidden');
})

home_page_signup_btn.addEventListener('click', async() => {
    loadPage();
    await timer(300);
    clearMain();
    signupPage.classList.remove('hidden');
})

nav_bar_home_btn.addEventListener('click', async() => {
    loadPage();
    await timer(500);
    clearMain();
    aboutPage.classList.remove('hidden');
})

nav_bar_profile_btn.addEventListener('click', async() => {
    loadPage();
    await timer(300);
    if (sessionInfo.logged == false) {
        clearMain();
        aboutPage.classList.remove('hidden');
    } else {
        clearMain();
        profilePage.classList.remove('hidden');
        loadProfile();
    }
})

nav_bar_contact_btn.addEventListener('click', async() => {
    loadPage();
    await timer(300);
    clearMain();
    contactPage.classList.remove('hidden');
})

nav_bar_about_btn.addEventListener('click', async() => {
    loadPage();
    await timer(300);
    clearMain();
    aboutPage.classList.remove('hidden');
})

nav_bar_dashboard_btn.addEventListener('click', async() => {
    loadPage();
    await timer(300);
    clearMain();
    dashboardPage.classList.remove('hidden');
    loadDashboard();
})

profile_page_logout_btn.addEventListener('click', () => {
    sessionInfo.logged = false;
    sessionInfo.currentUser = "";
    announce("Logged out successfully!")
    reloadLocal();
    clearMain();
    homePage.classList.remove('hidden');
});

async function timer(x) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(x);
      }, x);
    });
}

login_page_login_btn.addEventListener('click', async() => {
    let username = document.querySelector('#login-page-username');
    let password = document.querySelector('#login-page-password');
    if (username.value == "") {
        announce("Invalid username!");
        username.classList.add('error');
        await timer(2000);
        username.classList.remove('error');
    }
    if (password.value == "") {
        announce("Invalid password!");
        password.classList.add('error');
        await timer(2000);
        password.classList.remove('error');
    }
    login(username.value, password.value);
})

let tempSign = {
}

signup_page_singup_btn.addEventListener('click', () => {
    let first = document.querySelector('#signup-page-first-name');
    let last = document.querySelector('#signup-page-last-name');
    let username = document.querySelector('#signup-page-username');
    let password = document.querySelector('#signup-page-password');
    if (first.value == "" | last.value == "" | username.value == "" | password.value == "") {
        announce("Please fill all fields!");
        return;
    }
    tempSign.first = first.value;
    tempSign.last = last.value;
    tempSign.username = username.value;
    tempSign.password = password.value;
    signup(username.value);
})

signup_page_complete_btn.addEventListener('click', () => {
    let age = document.querySelector('#signup-page-age');
    let income = document.querySelector('#signup-page-income');
    let male = document.querySelector('#male');
    let female = document.querySelector('#female');
    let Dip = document.querySelector('#Dip');
    let UG = document.querySelector('#UG');
    let Grad = document.querySelector('#Grad');
    let PG = document.querySelector('#PG');
    if (age.value == "" | income.value == "") {
        announce("Please fill all fields!");
        return;
    }
    if (male.checked) {
        tempSign.gender = 'Male';
    } else {
        tempSign.gender = 'Female';
    }
    if (Dip.checked){
        tempSign.education = 'Diploma'
    } else if (UG.checked) {
        tempSign.education = 'Undergraduate'
    } else if (PG.checked) {
        tempSign.education = 'Postgraduate'
    } else {
        tempSign.education = 'Graduate'
    }
    completeSignup(age.value, income.value);
})

function login(username, password) {
    console.log(data)
    if (data.users.hasOwnProperty(username)) {
        if (data.users[username].password == password) {
            sessionInfo.logged = true;
            sessionInfo.currentUser = username;
            announce("Logged in successfully!")
            reloadLocal();
            clearMain();
            profilePage.classList.remove('hidden');
            loadProfile();
        }
    } else {
        announce("User does not exist, Sign up!")
    }
}

async function signup(username) {
    if (!data.users.hasOwnProperty(username)) {
        loadPage();
        await timer(300);
        clearMain();
        additionalPage.classList.remove('hidden');
    } else {
        announce("This username exists already!");
    }
}

async function completeSignup(age, income) {
    let user = {
        password : tempSign.password,
        total : 0,
        month : 0,
        goal : 0,
        income : tempSign.income,
        education : tempSign.education,
        information : {
            age : age,
            income : income,
            since : 2024,
            gender : tempSign.gender,
            score : 0,
            first : tempSign.first,
            last : tempSign.last
        }
    }
    data.users[tempSign.username] = user;
    reloadLocal();
    reloadData();
    announce("You are all set!");
    loadPage();
    await timer(300);
    clearMain();
    aboutPage.classList.remove('hidden');
    sendDataToBackend(user.income, user,education, user.information.age, user.information.gender);
}

async function announce(text) {
    announcer.textContent = text;
    announcer.classList.remove("hidden");
    await timer(2000);
    announcer.classList.add("hidden");
}

function sendDataToBackend(pocketMoney, educationLevel, age, gender) {
    const data = {
        pocketMoney: pocketMoney,
        educationLevel: educationLevel,
        age: age,
        gender: gender
    };

    fetch('http://127.0.0.1:5000/process_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(jsonData => {
        // Handle JSON response from backend
        console.log('Response from backend:', jsonData);
        // Process the response as needed
        data.users[tempSign.username].predictions = jsonData;
        reloadLocal();
        reloadData();
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error);
    });
}