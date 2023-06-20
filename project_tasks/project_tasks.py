from genshi.builder import tag
from trac.wiki.macros import WikiMacroBase


class ProjectTasksMacro(WikiMacroBase):
    _domain = "project_tasks"
    _description = "Provides a macro to display tasks for each project."

    def expand_macro(self, formatter, name, content, args=None):
        db = self.env.get_read_db()
        cursor = db.cursor()

        cursor.execute(
            """
            SELECT DISTINCT c.value AS project 
            FROM ticket_custom c 
            WHERE c.name = 'project' 
            AND c.ticket IN (SELECT id FROM ticket WHERE status <> 'closed');
        """
        )

        results = cursor.fetchall()

        projects = [result[0] for result in results]

        project_tasks = {}

        for project in projects:
            cursor.execute(
                """
                SELECT id, summary, status
                FROM ticket
                WHERE id IN (
                    SELECT ticket
                    FROM ticket_custom
                    WHERE name = 'project'
                    AND value = %s
                );
            """,
                (project,),
            )

            tasks = cursor.fetchall()
            project_tasks[project] = tasks

        div = tag.div(class_="project-tasks")

        # Sort projects before output
        for project, tasks in sorted(project_tasks.items()):
            div.append(tag.h2(project, class_="project-title"))
            ul = tag.ul(class_="task-list")

            for task in tasks:
                ul.append(
                    tag.li(
                        tag.a(
                            "#{}".format(task[0]), href=formatter.href.ticket(task[0])
                        ),
                        ": ",
                        task[1],
                        " (",
                        task[2],
                        ")",
                    )
                )

            div.append(ul)

        return div
