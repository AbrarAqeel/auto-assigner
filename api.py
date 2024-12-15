import mysql.connector
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)

host = 'localhost'
user = 'root'
pwd = '123321'
database = 'Meezanship'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=pwd,
        database=database
    )


@app.route('/')
def index():
    return render_template('index.html')


# Customer POV
@app.route('/customer-dashboard')
def customer_dashboard():
    return render_template("customer_dashboard.html")


@app.route('/submit-form', methods=['POST'])
def submit_form():
    form_type = request.form['Form_Type']
    form_detail = request.form['Form_Detail']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute(
                "INSERT INTO forms (Form_Type, Form_Detail) VALUES (%s, %s)",
                (form_type, form_detail)
            )
            conn.commit()
            return jsonify({'message': 'Form submitted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


# Supervisor POV
@app.route("/supervisor-dashboard", methods=['GET', 'POST'])
def manage_agents():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['Agent_Name']
        priority = request.form['Agent_Priority']
        workload = request.form['Agent_Workload']

        cursor.execute(
            "INSERT INTO agents (Agent_Name, Agent_Priority, Agent_Workload) VALUES (%s, %s, %s)",
            (name, priority, workload)
        )
        conn.commit()

    cursor.execute("SELECT * FROM agents WHERE visibility=1")
    agents = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('supervisor_dashboard.html', agents=agents)


@app.route('/update_agent_priority', methods=['POST'])
def update_agent_priority():
    agent_id = request.form['agent_id']
    new_priority = request.form['agent_priority']

    if not agent_id or not new_priority:
        return jsonify({'error': 'Agent priority is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("UPDATE agents SET agent_priority=%s WHERE agent_id=%s", (new_priority, agent_id))
            conn.commit()
            return jsonify({'message': 'Agent priority updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/update_agent_workload', methods=['POST'])
def update_agent_workload():
    agent_id = request.form['agent_id']
    new_workload = request.form['agent_workload']

    if not agent_id or not new_workload:
        return jsonify({'error': 'Agent ID and queue length are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("UPDATE agents SET agent_workload=%s WHERE agent_id=%s", (new_workload, agent_id))
            conn.commit()
            return jsonify({'message': 'Agent queue length updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/delete_agent', methods=['POST'])
def delete_agent():
    agent_id = request.form.get('agent_id')

    if not agent_id:
        return jsonify({'error': 'Agent ID is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("UPDATE Agents SET visibility=0 WHERE Agent_ID = %s", (agent_id,))
            conn.commit()

            if cursor.rowcount > 0:
                return jsonify({'message': 'Agent removed successfully'}), 200
            else:
                return jsonify({'error': 'No agent found with the given ID'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


# @app.route('/assign_forms', methods=['POST'])
# def assign_forms():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     else:
#         try:
#             # Get all available agents ordered by Priority (descending)
#             cursor.execute("SELECT * FROM agents WHERE Agent_Status='Available' ORDER BY Agent_Priority DESC")
#             agents = cursor.fetchall()
#
#             # Get all unassigned forms
#             cursor.execute("SELECT * FROM forms WHERE Form_Status='Unassigned'")
#             unassigned_forms = cursor.fetchall()
#
#             if not unassigned_forms:
#                 return jsonify({'message': 'No unassigned forms available'}), 404
#
#             # Round-robin index
#             round_robin_index = 0
#             num_agents = len(agents)
#
#             for form in unassigned_forms:
#                 assigned = False
#                 for _ in range(num_agents):
#                     agent = agents[round_robin_index]
#
#                     # Check if the agent's queue is full
#                     cursor.execute("SELECT COUNT(*) as count FROM Forms WHERE Assigned_Agent_ID=%s", (agent['Agent_ID'],))
#                     workload = cursor.fetchone()['count']
#
#                     if workload < agent['Agent_Workload']:
#                         # Assign the form to the agent
#                         cursor.execute("UPDATE forms SET Form_Status='Assigned', Assigned_Agent_ID=%s WHERE Form_ID=%s", (agent['Agent_ID'], form['Form_ID']))
#                         cursor.execute("UPDATE agents SET Agent_Status='Working' WHERE Agent_ID=%s", (agent['Agent_ID'],))
#                         conn.commit()
#                         assigned = True
#                         break
#
#                     # Move to the next agent in the round-robin order
#                     round_robin_index = (round_robin_index + 1) % num_agents
#
#                 if not assigned:
#                     # If no agent is available, leave the form unassigned
#                     continue
#
#             return jsonify({'message': 'Forms assigned to available agents successfully'}), 200
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
#         finally:
#             cursor.close()
#             conn.close()


"""         USE ME       """

@app.route('/assign_forms', methods=['POST'])
def assign_forms():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            # Get all available agents ordered by Priority (descending)
            cursor.execute("SELECT * FROM agents WHERE Visibility=1 AND Agent_Status='Available' ORDER BY Agent_Priority DESC")
            agents = cursor.fetchall()

            # Get all unassigned forms
            cursor.execute("SELECT * FROM forms WHERE Form_Status='Unassigned'")
            unassigned_forms = cursor.fetchall()

            if not unassigned_forms:
                return jsonify({'message': 'No unassigned forms available'}), 404

            # Round-robin index
            round_robin_index = 0
            num_agents = len(agents)

            for form in unassigned_forms:
                assigned = False
                for _ in range(num_agents):
                    agent = agents[round_robin_index]

                    # Check if the agent's queue is full
                    cursor.execute("SELECT COUNT(*) as count FROM Forms WHERE Assigned_Agent_ID=%s", (agent['Agent_ID'],))
                    workload = cursor.fetchone()['count']

                    if workload < agent['Agent_Workload']:
                        # Assign the form to the agent
                        cursor.execute("UPDATE forms SET Form_Status='Assigned', Assigned_Agent_ID=%s WHERE Form_ID=%s", (agent['Agent_ID'], form['Form_ID']))
                        cursor.execute("UPDATE agents SET Agent_Status='Working' WHERE Agent_ID=%s", (agent['Agent_ID'],))
                        conn.commit()
                        assigned = True
                        break

                    # Move to the next agent in the round-robin order
                    round_robin_index = (round_robin_index + 1) % num_agents

                if not assigned:
                    # If no agent is available, leave the form unassigned
                    continue

            return jsonify({'message': 'Forms assigned to available agents successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/agents_status', methods=['GET'])
def get_agents_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("SELECT Agent_ID, Agent_Status FROM agents")
            agents = cursor.fetchall()
            return jsonify({'agents': agents}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/form_status', methods=['GET'])
def get_form_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("SELECT Form_ID, Form_Status, Assigned_Agent_Name FROM forms")
            forms = cursor.fetchall()
            return jsonify({'forms': forms}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/forms', methods=['GET'])
def get_forms():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("SELECT * FROM forms")
            forms = cursor.fetchall()
            return jsonify(forms), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


# Agent Dashboard
@app.route('/agent-login')
def agent_login_form():
    return render_template("agent_login_form.html")


# Agent Dashboard
@app.route('/agent_login', methods=['POST'])
def agent_login():
    username = request.form['username']
    password = request.form['password']
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    else:
        try:
            cursor.execute("SELECT * FROM Agents_Login WHERE Username=%s AND Password=%s", (username, password))
            agent = cursor.fetchone()
            if agent:
                session['agent_id'] = agent['Agent_ID']
                return redirect(url_for('agent_dashboard'))
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()


@app.route('/')
def agent_dashboard():
    return render_template('agent_dashboard.html')


@app.route('/get_agent_info')
def get_agent_info():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT Agent_ID, Agent_Name, Agent_Status FROM Agents WHERE Agent_ID = 1")
    agent_info = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(agent_info)


@app.route('/get_form_details')
def get_form_details():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT Form_ID, Form_Type, Form_Detail FROM Forms WHERE Form_Status = 'Assigned' LIMIT 1")
    form_details = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(form_details)


@app.route('/get_workload')
def get_workload():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT Agent_Workload FROM Agents WHERE Agent_ID = 1")
    workload = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(workload)


@app.route('/update_status', methods=['POST'])
def update_status():
    new_status = request.json.get('status')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE Agents SET Agent_Status = %s WHERE Agent_ID = 1", (new_status,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'success': True})


@app.route('/complete_form', methods=['POST'])
def complete_form():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Forms SET Form_Status = 'Completed' "
        "WHERE Form_ID = (SELECT Form_ID FROM Forms WHERE Assigned_Agent_ID = 1)")
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'success': True})


@app.route("/agent-dashboard", methods=['GET', 'POST'])
def manage_agent_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        agent_id = request.form.get('Agent_ID')
        agent_status = request.form.get('Agent_Status')

        # Update the agent's status
        cursor.execute(
            """
            UPDATE Agents
            SET Agent_Status = %s
            WHERE Agent_ID = %s
            """,
            (agent_status, agent_id)
        )
        conn.commit()

    # Fetching the agent's details and form details
    cursor.execute(
        """
        SELECT
            Agents.Agent_ID,
            Agents.Agent_Name,
            Agents.Agent_Status,
            Forms.Form_ID,
            Forms.Form_Type,
            Forms.Form_Detail AS Form_Description,
            (SELECT COUNT(*) FROM Forms WHERE Form_Status = 'Unassigned') AS Pending_Forms_Queue
        FROM
            Agents
            
        LEFT JOIN
            Forms
        ON
            Agents.Agent_ID = Forms.Assigned_Agent_ID
        WHERE
            Agents.Agent_ID = %s
        """,
        (1,)  # Replace with dynamic Agent_ID if needed
    )

    agent_dash = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('agent_dashboard.html', agent_dashboard=agent_dash)


if __name__ == '__main__':
    app.run(debug=True)
