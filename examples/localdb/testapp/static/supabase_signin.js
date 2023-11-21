/**
 * JS handlers for the Django 'supabase_signin.html' template.
 */

var supabase = supabase.createClient(
     // URL and key are passed from the Django template
    document.currentScript.dataset.supabaseUrl,
    document.currentScript.dataset.supabaseKey,
);

async function signInGithub() {
    const { data, error } = supabase.auth.signInWithOAuth({
        provider: "github",
    });
    if (error) {
        showMessage(error, "error");
        return;
    }
    showMessage("Sign in started. Redirecting to GitHub...");
}

async function signInOtp() {
    const email = document.getElementById("id_email").value;
    const { data, error } =  await supabase.auth.signInWithOtp({
        email: email,
    });
    if (error) {
        showMessage(error, "error");
        return;
    }
    showMessage(`Please follow the link sent to '${email}' to sign in.`);
}

async function signOut() {
    const { error } = await supabase.auth.signOut();
    if (error) {
        showMessage(error, "error");
        return;
    }
    showMessage("Supabase Sign out completed. Reloading the page ...");
    window.location.reload();
}

/**
* Get user data encoded in token from the Django endpoint.
* @param  {String} accessToken token to use to authenticate the request.
* @returns {Object}
*/
async function fetchUser(accessToken) {
  try {
      const response = await fetch("/auth", {
          headers: new Headers({
              "Authorization": `Bearer ${accessToken}`,
              "Content-Type": "application/json",
          })
      });
      if (!response.ok) {
          console.log(response);
          showMessage(`Django endpoint response: ${response.status} - ${response.statusText}`, "error")
          throw new Error("Error fetching user data from the Django endpoint.");
      }
      const data = await response.json();
      return { data, error: null };
  } catch (error) {
      return { data: null, error };
  }
}

function showMessage(text, tag="success") {
    const logger = tag === "error" ? console.error : console.log;
    logger(text);
    const messages = document.querySelector(".messagelist");
    const item = document.createElement("li");
    item.textContent = text;
    item.classList.add(tag);
    messages.appendChild(item);
}

function toggleHidden(selector) {
    document.querySelectorAll(selector).forEach(function(element) {
        element.classList.toggle("hidden");
    });
}

document.addEventListener("DOMContentLoaded", async (event) => {
    console.log(supabase);
    let { data, error } = await supabase.auth.getSession()
    if (error) {
        showMessage(error, "error");
        return;
    }
    let sessionData = data;
    if (sessionData?.session) {
        const token = sessionData.session.access_token;
        showMessage("Supabase session is available. Loading user data from Django endpoint ...");
        console.log(sessionData.session);
        console.log(`Supabase access token: ${token}`);
        let { data, error }  = await fetchUser(token);
        if (error) {
            showMessage(error, "error");
            return;
        }
        const userData = data;
        showMessage("Decoded user information received from the Django endpoint.");
        document.getElementById("id_user").textContent = JSON.stringify(userData, null, 4);
        toggleHidden(".sign-out");
    } else {
        toggleHidden(".sign-in");
    }
});
