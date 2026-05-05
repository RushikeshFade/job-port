const API = "http://127.0.0.1:8000"

async function registerUser(){
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const role = document.getElementById("role").value

    const res = await fetch(`${API}/register`,{
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({email,password,role})
    })

    const data = await res.json()
    alert(data.message || "Registered")
}

async function loginUser(){
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    const form = new URLSearchParams()
    form.append("username",email)
    form.append("password",password)

    const res = await fetch(`${API}/login`,{
        method:"POST",
        body:form
    })

    const data = await res.json()

    if(data.access_token){
        localStorage.setItem("token",data.access_token)
        window.location.href="dashboard.html"
    }else{
        alert("Login failed")
    }
}

async function loadJobs(){
    const res = await fetch(`${API}/jobs`)
    const jobs = await res.json()

    const container = document.getElementById("jobs")

    jobs.forEach(job=>{
        const div=document.createElement("div")
        div.className="card"

        div.innerHTML=`
        <h3>${job.title}</h3>
        <p>${job.description}</p>
        <p>${job.location}</p>
        <p>${job.salary}</p>
        <button onclick="applyJob(${job.id})">Apply</button>
        `

        container.appendChild(div)
    })
}

async function applyJob(id){

    const token=localStorage.getItem("token")

    const res=await fetch(`${API}/apply/${id}`,{
        method:"POST",
        headers:{
            Authorization:`Bearer ${token}`
        }
    })

    const data=await res.json()

    alert(data.message || "Applied")
}

async function postJob(){

    const token=localStorage.getItem("token")

    const title=document.getElementById("title").value
    const description=document.getElementById("description").value
    const location=document.getElementById("location").value
    const salary=document.getElementById("salary").value

    const res=await fetch(`${API}/jobs`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            Authorization:`Bearer ${token}`
        },
        body:JSON.stringify({
            title,description,location,salary
        })
    })

    const data=await res.json()

    alert(data.message || "Job posted")
}