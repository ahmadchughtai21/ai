import React, { useEffect, useMemo, useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import TodoWorkspace from './TodoWorkspace';
import { getAuthStatus, getCsrfToken, login, logout, signup } from './services/api';
import './styles/App.css';

const ROUTES = {
  home: '/',
  login: '/login',
  signup: '/signup',
  app: '/app',
};

function navigate(path) {
  if (window.location.pathname !== path) {
    window.history.pushState({}, '', path);
  }
}

function flattenErrors(errors) {
  if (!errors || typeof errors !== 'object') return 'Something went wrong.';
  return Object.entries(errors)
    .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(' ') : msgs}`)
    .join(' | ');
}

function LandingPage({ onLoginClick, onSignupClick }) {
  return (
    <div className="marketing-page">
      <header className="marketing-nav">
        <div className="marketing-nav-inner">
          <div className="marketing-brand">✓ TackTack</div>
          <nav className="marketing-nav-links">
            <a href="#highlights">Highlights</a>
            <a href="#workflow">How it works</a>
            <a href="#faq">FAQ</a>
          </nav>
          <div className="marketing-nav-actions">
            <a
              className="marketing-btn ghost marketing-github-link"
              href="https://github.com/ahmadchughtai21/ai_todo"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
            <button className="marketing-btn ghost" onClick={onLoginClick}>Log in</button>
            <button className="marketing-btn primary" onClick={onSignupClick}>Get Started</button>
          </div>
        </div>
      </header>
      <main className="marketing-main">
        <section className="marketing-hero marketing-animate">
          <div className="marketing-animate delay-1">
            <span className="marketing-kicker">Your daily planning space</span>
            <h1>A calm, modern todo app that helps you stay in flow.</h1>
            <p>
              Quickly capture tasks, organize your work, and plan your week with a clean interface
              built for focus.
            </p>
            <div className="marketing-cta">
              <button className="marketing-btn primary" onClick={onSignupClick}>Start free</button>
              <button className="marketing-btn ghost" onClick={onLoginClick}>Log in</button>
            </div>
            <div className="marketing-inline-stats">
              <div><strong>Fast capture</strong><span>Add tasks in seconds with forms or AI chat</span></div>
              <div><strong>Clear planning</strong><span>See Inbox, Today, and Next 7 Days instantly</span></div>
              <div><strong>Built to focus</strong><span>Minimal multi-pane layout with dark and light theme</span></div>
            </div>
          </div>
          <div className="marketing-card marketing-animate delay-2">
            <h3>Everything in one workspace</h3>
            <p>Use the app the way you prefer:</p>
            <ul>
              <li>Manual task creation and editing</li>
              <li>AI chat commands for quick planning</li>
              <li>Categories, tags, priority, due dates</li>
              <li>Subtasks and file attachments</li>
              <li>Recurring tasks for routines</li>
              <li>Simple smart views for daily planning</li>
            </ul>
          </div>
        </section>

        <section className="marketing-section marketing-animate delay-2" id="highlights">
          <div className="marketing-section-head">
            <h2>Highlights</h2>
            <p>Designed to help you plan clearly without noise.</p>
          </div>
          <div className="marketing-feature-grid">
            <article className="marketing-feature-card">
              <h4>AI assistant</h4>
              <p>Type natural language to create, update, or organize tasks.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>Manual control</h4>
              <p>Use clean forms for tasks, categories, subtasks, and attachments.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>Smart views</h4>
              <p>Switch between Inbox, Today, and Next 7 Days with one click.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>Recurring tasks</h4>
              <p>Set daily, weekly, monthly, or yearly recurrence for repeating work.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>Task details</h4>
              <p>Keep notes, subtasks, due times, tags, and attachments together.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>Theme and layout</h4>
              <p>Work in a calm multi-pane interface with dark and light modes.</p>
            </article>
          </div>
        </section>

        <section className="marketing-section marketing-animate delay-3" id="workflow">
          <div className="marketing-section-head">
            <h2>How it works</h2>
            <p>Simple flow from idea to execution.</p>
          </div>
          <div className="marketing-security-grid">
            <article className="marketing-feature-card">
              <h4>1. Capture</h4>
              <p>Add tasks manually or ask the AI assistant in plain language.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>2. Organize</h4>
              <p>Group tasks by category, set priority, due date, tags, and subtasks.</p>
            </article>
            <article className="marketing-feature-card">
              <h4>3. Execute</h4>
              <p>Review Today/Next 7 Days, complete tasks, and keep momentum.</p>
            </article>
          </div>
        </section>

        <section className="marketing-section marketing-animate delay-3" id="faq">
          <div className="marketing-section-head">
            <h2>Frequently asked questions</h2>
          </div>
          <div className="marketing-faq-list">
            <article className="marketing-faq-item">
              <h4>Can I use both AI and manual task management?</h4>
              <p>Yes. You can switch between chat commands and manual forms anytime.</p>
            </article>
            <article className="marketing-faq-item">
              <h4>Can I plan recurring work?</h4>
              <p>Yes. Recurrence is available for daily, weekly, monthly, and yearly tasks.</p>
            </article>
            <article className="marketing-faq-item">
              <h4>Is there dark mode?</h4>
              <p>Yes. The workspace includes both dark and light themes.</p>
            </article>
          </div>
        </section>

        <section className="marketing-final-cta marketing-animate delay-4">
          <h2>Start planning better in minutes</h2>
          <p>Create your workspace and keep your work, study, and personal goals in one secure place.</p>
          <div className="marketing-cta">
            <button className="marketing-btn primary" onClick={onSignupClick}>Get Started Free</button>
            <button className="marketing-btn ghost" onClick={onLoginClick}>Log in</button>
          </div>
        </section>
      </main>

      <footer className="marketing-footer">
        <div className="marketing-footer-inner">
          <div className="marketing-footer-brand">✓ TackTack</div>
          <div className="marketing-footer-links">
            <a href="#highlights">Highlights</a>
            <a href="#workflow">How it works</a>
            <a href="#faq">FAQ</a>
            <a href="https://github.com/ahmadchughtai21/ai_todo" target="_blank" rel="noopener noreferrer">GitHub</a>
          </div>
          <div className="marketing-footer-copy">© {new Date().getFullYear()} TackTack. All rights reserved.</div>
        </div>
      </footer>
    </div>
  );
}

function AuthForm({
  mode,
  onSubmit,
  onSwitchMode,
  loading,
  error,
}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');

  const isSignup = mode === 'signup';

  const title = isSignup ? 'Create your account' : 'Welcome back';
  const subtitle = isSignup
    ? 'Start your private TackTack workspace.'
    : 'Log in to continue to your workspace.';

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isSignup) {
      onSubmit({ username, password, passwordConfirm });
      return;
    }
    onSubmit({ username, password });
  };

  return (
    <div className="auth-shell">
      <header className="auth-shell-header">
        <div className="auth-shell-inner">
          <a className="auth-shell-brand" href="/">✓ TackTack</a>
          <div className="auth-shell-actions">
            <a
              className="auth-shell-link"
              href="https://github.com/ahmadchughtai21/ai_todo"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
          </div>
        </div>
      </header>

      <main className="auth-page">
        <div className="auth-card">
          <h1>{title}</h1>
          <p>{subtitle}</p>
          {error && <div className="auth-error">{error}</div>}
          <form onSubmit={handleSubmit}>
            <label>Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} required />

            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />

            {isSignup && (
              <>
                <label>Confirm Password</label>
                <input
                  type="password"
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                  required
                />
              </>
            )}

            <button type="submit" disabled={loading}>
              {loading ? 'Please wait...' : isSignup ? 'Create account' : 'Log in'}
            </button>
          </form>

          <div className="auth-switch">
            {isSignup ? 'Already have an account?' : 'New here?'}{' '}
            <button type="button" className="auth-switch-link" onClick={onSwitchMode}>
              {isSignup ? 'Log in' : 'Create account'}
            </button>
          </div>
        </div>
      </main>

      <footer className="auth-shell-footer">
        <div className="auth-shell-inner">
          <span>© {new Date().getFullYear()} TackTack</span>
          <a className="auth-shell-link" href="/">Home</a>
        </div>
      </footer>
    </div>
  );
}

function App() {
  const [path, setPath] = useState(window.location.pathname);
  const [authLoading, setAuthLoading] = useState(true);
  const [authActionLoading, setAuthActionLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [authError, setAuthError] = useState('');

  const refreshAuth = async () => {
    await getCsrfToken();
    const status = await getAuthStatus();
    if (status.data?.authenticated) {
      setUser({ username: status.data.username });
    } else {
      setUser(null);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        await refreshAuth();
      } catch (e) {
        setUser(null);
      } finally {
        setAuthLoading(false);
      }
    };
    init();

    const onPopState = () => setPath(window.location.pathname);
    const onUnauthorized = () => {
      setUser(null);
      setAuthError('Your session expired. Please log in again.');
      navigate(ROUTES.login);
      setPath(ROUTES.login);
    };

    window.addEventListener('popstate', onPopState);
    window.addEventListener('auth:unauthorized', onUnauthorized);
    return () => {
      window.removeEventListener('popstate', onPopState);
      window.removeEventListener('auth:unauthorized', onUnauthorized);
    };
  }, []);

  const handleLogin = async ({ username, password }) => {
    setAuthActionLoading(true);
    setAuthError('');
    try {
      await getCsrfToken();
      const response = await login(username, password);
      await getCsrfToken();
      setUser({ username: response.data.username });
      navigate(ROUTES.app);
      setPath(ROUTES.app);
    } catch (e) {
      setAuthError(flattenErrors(e.response?.data?.errors));
    } finally {
      setAuthActionLoading(false);
    }
  };

  const handleSignup = async ({ username, password, passwordConfirm }) => {
    setAuthActionLoading(true);
    setAuthError('');
    try {
      await getCsrfToken();
      const response = await signup(username, password, passwordConfirm);
      await getCsrfToken();
      setUser({ username: response.data.username });
      navigate(ROUTES.app);
      setPath(ROUTES.app);
    } catch (e) {
      setAuthError(flattenErrors(e.response?.data?.errors));
    } finally {
      setAuthActionLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await getCsrfToken();
      await logout();
      await getCsrfToken();
    } finally {
      setUser(null);
      navigate(ROUTES.home);
      setPath(ROUTES.home);
    }
  };

  const currentView = useMemo(() => {
    if (path === ROUTES.login) return 'login';
    if (path === ROUTES.signup) return 'signup';
    if (path === ROUTES.app) return 'app';
    return 'home';
  }, [path]);

  useEffect(() => {
    if (user && currentView !== 'app') {
      navigate(ROUTES.app);
      setPath(ROUTES.app);
    }
  }, [user, currentView]);

  if (authLoading) {
    return <div className="auth-loading">Loading...</div>;
  }

  if (!user) {
    if (currentView === 'login') {
      return (
        <AuthForm
          mode="login"
          onSubmit={handleLogin}
          onSwitchMode={() => {
            setAuthError('');
            navigate(ROUTES.signup);
            setPath(ROUTES.signup);
          }}
          loading={authActionLoading}
          error={authError}
        />
      );
    }

    if (currentView === 'signup') {
      return (
        <AuthForm
          mode="signup"
          onSubmit={handleSignup}
          onSwitchMode={() => {
            setAuthError('');
            navigate(ROUTES.login);
            setPath(ROUTES.login);
          }}
          loading={authActionLoading}
          error={authError}
        />
      );
    }

    return (
      <LandingPage
        onLoginClick={() => {
          setAuthError('');
          navigate(ROUTES.login);
          setPath(ROUTES.login);
        }}
        onSignupClick={() => {
          setAuthError('');
          navigate(ROUTES.signup);
          setPath(ROUTES.signup);
        }}
      />
    );
  }

  if (currentView !== 'app') return null;

  return (
    <ThemeProvider>
      <TodoWorkspace user={user} onLogout={handleLogout} />
    </ThemeProvider>
  );
}

export default App;
