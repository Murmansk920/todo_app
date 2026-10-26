// 登录：成功后把 Token 存起来，刷新页面也不丢
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    try {
        const data = await api("/login", { method: "POST", body: { username, password } });
        localStorage.setItem("token", data.token);
        loadTodos();          // 登录成功 → 加载任务列表
    } catch (e) {
        alert("登录失败：" + e.message);   // 401 会走到这里
    }
}

// 加载任务列表，并画到页面上
async function loadTodos() {
    const list = document.getElementById("todo-list");
    try {
        const data = await api("/todos");
        list.innerHTML = data.todos.                    // [{id,title,completed},...]
            map(t => `<li>
                <input type="checkbox" ${t.completed ? "checked" : ""}
                       onchange="toggleTodo(${t.id}, this.checked)">
                ${t.title}
                <button onclick="deleteTodo(${t.id})">删除</button>
            </li>`).join("");
    } catch (e) {
        if (e.message.includes("过期")) {          // Token 过期 → 回登录界面
            localStorage.removeItem("token");
            alert("登录已过期，请重新登录");
        }
    }
}