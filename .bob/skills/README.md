# Bob Skills for IBM Optim Archive

This directory contains two specialized skills for working with IBM Optim Archive:

## Available Skills

### 1. Optim Dashboard Creator (`optim-dashboard`)
**Description**: Help users create, customize, and troubleshoot IBM Optim Archive BI dashboards with real-time monitoring and analytics

**Use this skill when you need to**:
- Create new dashboard visualizations
- Modify existing dashboard components
- Add new metrics or charts
- Troubleshoot dashboard issues
- Customize the BI dashboard

**Supporting files**:
- `dashboard-setup-guide.md` - Setup and configuration instructions
- `dashboard-api-reference.md` - Dashboard API endpoints documentation

### 2. Optim API Helper (`optim-api`)
**Description**: Help users interact with IBM Optim Archive API for authentication, job management, archive access, and data retrieval

**Use this skill when you need to**:
- Work with the Optim Archive API
- Authenticate and manage tokens
- List and manage archive jobs
- Access archived data
- Query archive schemas and tables
- Export data from archives

**Supporting files**:
- `api-endpoints.md` - Complete API endpoint reference

## How Skills Work

Skills are automatically activated by Bob when relevant to your request. You can also explicitly request a skill by mentioning it in your message.

**Example requests**:
- "Help me add a new chart to the dashboard" → Activates `optim-dashboard`
- "How do I list all archive jobs using the API?" → Activates `optim-api`
- "I need to export data from an archive" → Activates `optim-api`

## Skill Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md                    # Main skill instructions (required)
└── supporting-files.md         # Reference documentation (optional)
```

## Requirements

- Skills are only available in **Advanced mode**
- Skills load once per conversation
- Bob automatically determines when to activate skills based on your request

## Customization

You can modify the skills by editing the `SKILL.md` files. Changes take effect in new conversations.

## Related Files

The skills reference these project files:
- `auth_helper.py` - Authentication helper
- `demo_optim_api.py` - API demo script
- `dashboard/` - Dashboard implementation
- `docs/API_REFERENCE.md` - API documentation
- `examples/` - Usage examples