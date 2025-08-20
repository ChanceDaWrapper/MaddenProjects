import json
import csv
import os
from flask import Flask, request, make_response, jsonify, send_file


# python maddenupload.py



app = Flask(__name__)

# Directory to store CSV files
CSV_DIR = "exported_csv"
os.makedirs(CSV_DIR, exist_ok=True)

# Helper function to save data to CSV
def save_to_csv(filename, data):
    try:
        # Ensure directory exists
        os.makedirs(CSV_DIR, exist_ok=True)
        file_path = os.path.join(CSV_DIR, filename)

        # Check if data is a non-empty list of dictionaries
        if isinstance(data, list) and data:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data[0].keys())  # Write header row
                for row in data:
                    writer.writerow(row.values())  # Write data rows
        else:
            raise ValueError("Data is not a valid list of dictionaries.")

        print(f"Data successfully saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error in save_to_csv: {e}")  # Log the error
        return None



# Endpoint for league teams
@app.route('/<platform>/<cfm_id>/leagueteams', methods=['POST'])
def export_league_teams(platform, cfm_id):
    req_data = request.get_json()
    print(f"Request data received: {req_data}")

    # Extract the "leagueTeamInfoList" from the payload
    data_to_save = req_data.get("leagueTeamInfoList", [])
    
    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'leagueteams_{cfm_id}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
        return jsonify({'error': 'Failed to save data'}), 500
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list under "leagueTeamInfoList".'}), 400

# Endpoint for standings
@app.route('/<platform>/<cfm_id>/standings', methods=['POST'])
def export_standings(platform, cfm_id):
    req_data = request.get_json()
    # Extract the "teamStandingInfoList" from the payload
    data_to_save = req_data.get("teamStandingInfoList", [])
    
    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'standings_{cfm_id}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
        return jsonify({'error': 'Failed to save data'}), 500
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list under "teamStandingInfoList".'}), 400

# Endpoint for free agents
@app.route('/<platform>/<cfm_id>/freeagents/roster', methods=['POST'])
def export_freeagents(platform, cfm_id):
    req_data = request.get_json()
    # print(f"Received JSON for free agents: {req_data}")

    # Validate payload
    if not req_data:
        return jsonify({'error': 'Empty or invalid JSON payload'}), 400

    # Extract rosterInfoList
    data_to_save = req_data.get('rosterInfoList', None)

    # If rosterInfoList is empty, log and return success
    if not isinstance(data_to_save, list) or not data_to_save:
        # print("Invalid or empty rosterInfoList:", data_to_save)
        return jsonify({'message': 'No free agents to process. Skipping.'}), 200

    # Save data to CSV
    file_path = save_to_csv(f'free_agents_{cfm_id}.csv', data_to_save)
    if file_path:
        # print(f"Data saved successfully to {file_path}")
        return jsonify({'message': f'Data saved to {file_path}'}), 200

    # print("Failed to save data to CSV.")
    return jsonify({'error': 'Failed to save data'}), 500

# Endpoint for rosters
@app.route('/<platform>/<cfm_id>/team/<team_id>/roster', methods=['POST'])
def export_roster(platform, cfm_id, team_id):
    req_data = request.get_json()

    # Validate payload
    if not req_data:
        return jsonify({'error': 'Empty or invalid JSON payload'}), 400
    
    # Extract the "rosterInfoList" from the payload
    data_to_save = req_data.get('rosterInfoList', [])

    # If rosterInfoList is empty, skip saving and return a success message
    if not isinstance(data_to_save, list) or not data_to_save:
        # print("rosterInfoList is empty. Skipping save operation.")
        return jsonify({'message': 'No free agents to process. Skipping.'}), 200
        

    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'{team_id}_roster_{cfm_id}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
        return jsonify({'error': 'Failed to save data'}), 500
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list under "rosterInfoList".'}), 400




# Endpoint for punting
@app.route('/<platform>/<cfm_id>/week/reg/<week>/punting', methods=['POST'])
def export_punting(platform, cfm_id, week):
    req_data = request.get_json()
    data_to_save = req_data.get('playerPuntingStatInfoList', [])


    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'punting_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400


# Endpoint for passing
@app.route('/<platform>/<cfm_id>/week/reg/<week>/passing', methods=['POST'])
def export_passing(platform, cfm_id, week):
    req_data = request.get_json()
    print(req_data.keys())
    data_to_save = req_data.get('playerPassingStatInfoList', [])

    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'passing_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400


# Endpoint for rushing
@app.route('/<platform>/<cfm_id>/week/reg/<week>/rushing', methods=['POST'])
def export_rushing(platform, cfm_id, week):
    req_data = request.get_json()
    print(req_data.keys())
    data_to_save = req_data.get('playerRushingStatInfoList', [])


    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'rushing_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400


# Endpoint for receiving
@app.route('/<platform>/<cfm_id>/week/reg/<week>/receiving', methods=['POST'])
def export_receiving(platform, cfm_id, week):
    req_data = request.get_json()
    print(req_data.keys())
    data_to_save = req_data.get('playerReceivingStatInfoList', [])


    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'receiving_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400


# Endpoint for kicking
@app.route('/<platform>/<cfm_id>/week/reg/<week>/kicking', methods=['POST'])
def export_kicking(platform, cfm_id, week):
    req_data = request.get_json()
    print(req_data.keys())
    data_to_save = req_data.get('playerKickingStatInfoList', [])


    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'kicking_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400


# Endpoint for defense
@app.route('/<platform>/<cfm_id>/week/reg/<week>/defense', methods=['POST'])
def export_defense(platform, cfm_id, week):
    req_data = request.get_json()
    print(req_data.keys())
    data_to_save = req_data.get('playerDefensiveStatInfoList', [])

    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'defense_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400




# Endpoint for schedules
@app.route('/<platform>/<cfm_id>/week/reg/<week>/schedules', methods=['POST'])
def export_schedules(platform, cfm_id, week):
    req_data = request.get_json()
    
    # Validate payload
    if not req_data:
        return jsonify({'error': 'Empty or invalid JSON payload'}), 400
    
    # Extract the "gameScheduleInfoList" from the payload
    data_to_save = req_data.get('gameScheduleInfoList', [])

    # If gameScheduleInfoList is empty, skip saving and return a success message
    if not isinstance(data_to_save, list) or not data_to_save:
        # print("gameScheduleInfoList is empty. Skipping save operation.")
        return jsonify({'message': 'No free agents to process. Skipping.'}), 200
        

    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'week_{week}_stats_{cfm_id}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
        return jsonify({'error': 'Failed to save data'}), 500
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list under "gameScheduleInfoList".'}), 400



# Endpoint for team stats
@app.route('/<platform>/<cfm_id>/week/reg/<week>/teamstats', methods=['POST'])
def export_teamstats(platform, cfm_id, week):
    req_data = request.get_json()
    # print(f'Madden League ID: {cfm_id}')
    # print(f'Madden League Week: {week}')
    # print(f'Received JSON for team stats: {req_data}')

    data_to_save = req_data.get('teamStatInfoList', [])


    if isinstance(data_to_save, list) and data_to_save:
        file_path = save_to_csv(f'teamstats_{cfm_id}_week{week}.csv', data_to_save)
        if file_path:
            return jsonify({'message': f'Data saved to {file_path}'}), 200
    return jsonify({'error': 'Invalid data format or empty list. Expected a non-empty list.'}), 400

# Route to download CSV files
@app.route('/download/<filename>', methods=['GET'])
def download_csv(filename):
    file_path = os.path.join(CSV_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)