from db_analysis_utilities import *
from analysis_functions import *

from db_analysis_utilities import *
from analysis_functions import *


with DatabaseInstance() as db:
    id_input = input("Please enter all config IDs separated by spaces: ")
    config_ids = [int(id.strip()) for id in id_input.split()]

    print(
        "--------------------------------------------------------------------------------------"
    )
    print("You have entered the following IDs:", config_ids)
    print(
        "--------------------------------------------------------------------------------------"
    )

    print("Which plotting configuration would you like to have for all IDs?")
    print(
        "Press 1 for Firing, press 2 for CF FSS, press 3 for CF with LOX, press 4 for Ignition, press 5 for Efficiency"
    )
    config_opt = int(input("Enter configuration: "))
    print("You have chosen configuration:", config_opt)
    print(
        "--------------------------------------------------------------------------------------"
    )

    for id in config_ids:
        print(f"Processing ID: {id}")
        print(
            "--------------------------------------------------------------------------------------"
        )
        if config_opt == 1:
            print("FIRING CONFIGURATION")
            # Firing configuration
            # --- Plot 1: Mass Flow and Thrust ---
            # sensors1 = ["oss_mf", "fss_mf", "eng_lc", "ign_p", "rnl_oss_t"]
            # sensors_n1 = [
            #     "OSS Mass Flow /10",
            #     "FSS Mass Flow /10",
            #     "Thrust /10",
            #     "Igniter Pressure",
            #     "OSS Temperature below tank",
            # ]
            # yaxis1 = ["Mass Flow in g/s", "Temperature in C"]

            # analysis1 = Analysis_Instance(db, config_ids, sensors1, yaxis1)
            # print(analysis1.event_list)
            # print(analysis1.firing_starts[id])

            # start1 = analysis1.starts[id]
            # end1 = analysis1.ends[id]

            # fig1 = make_subplots(specs=[[{"secondary_y": True}]])
            # for i, sensor in enumerate(analysis1.sensors_values[id]):
            #     sensor_name = analysis1.sensors[i]
            #     values = analysis1.sensors_values[id][sensor]
            #     sensor_cut = values[
            #         (values["timestamp"] >= start1) & (values["timestamp"] <= end1)
            #     ]
            #     sensor_cut["time"] = pd.to_datetime(
            #         sensor_cut["timestamp"] + 3600 * 2, unit="s"
            #     )
            #     sensor_cut["time_relative"] = sensor_cut["timestamp"] - start1
            #     if i < 8:  # 8 sensors for example
            #         if i < 3:  # the 3 first sensors
            #             fig1.add_trace(
            #                 go.Scatter(
            #                     x=sensor_cut["time"],
            #                     y=sensor_cut["value"].rolling(30).mean() / 10,
            #                     name=sensors_n1[i],
            #                 ),
            #                 secondary_y=False,
            #             )
            #         # elif i==10:
            #         #     fig1.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean()/10, name=sensors_n1[i]), secondary_y= False)
            #         #     #fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']/10, name=sensors_n[i]), secondary_y= False)
            #         else:
            #             # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= False)
            #             fig1.add_trace(
            #                 go.Scatter(
            #                     x=sensor_cut["time"],
            #                     y=sensor_cut["value"].rolling(30).mean(),
            #                     name=sensors_n1[i],
            #                 ),
            #                 secondary_y=True,
            #             )
            #     else:
            #         # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= True)
            #         # if i == 11:
            #         #     fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']-222, name=sensors_n[i]), secondary_y= True)
            #         # else:
            #         fig1.add_trace(
            #             go.Scatter(
            #                 x=sensor_cut["time"],
            #                 y=sensor_cut["value"],
            #                 name=sensors_n1[i],
            #             ),
            #             secondary_y=True,
            #         )
            # # fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')

            # for i, event in enumerate(analysis1.event_list[id]):

            #     if isinstance(event, list):
            #         if len(event) == 0:
            #             print("empty")
            #     else:
            #         if isinstance(event, list):
            #             event = event[0]
            #         event_name = analysis1.event_names[id][i]
            #         if event - start1 >= 0 and event - end1 <= 0:
            #             x = pd.to_datetime(event, unit="s")
            #             x = event * 1000
            #             # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
            #             fig1.add_vline(
            #                 x=x,
            #                 line_width=1,
            #                 line_dash="dash",
            #                 line_color="white",
            #                 annotation_text=event_name,
            #             )
            #             # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

            # y = []
            # for i, a in enumerate(fig1.to_dict()["layout"]["annotations"]):
            #     y.append([a, 0.95 - (i % 15) * 0.05])

            # fig1.update_layout(
            #     annotations=[{**element[0], **{"y": element[1]}} for element in y]
            # )
            # fig1.update_yaxes(title_text=yaxis1[0], secondary_y=False)
            # fig1.update_yaxes(title_text=yaxis1[1], secondary_y=True)
            # # fig.update_yaxes(title_text = yaxis[0])
            # fig1.show()
            # filepath = (
            #     "/home/dacs/git/data-management/database_pro/simpleplot_%s.html"
            #     % (str(analysis1.dates[id]))
            # )
            # i = 0
            # while os.path.exists(filepath):
            #     filepath = (
            #         "/home/dacs/git/data-management/database_pro/simpleplot_%s_%s.html"
            #         % (str(analysis1.dates[id]), str(i))
            #     )
            #     i = i + 1
            # fig1.write_html(filepath)

        # -----------------------------------------------------------------------------------------------------------------------------------------------------
        # FSS COLD FLOW CONFIGURATION
        #
        #   THIS PART MAKES TWO PLOTS
        #       ONE PLOT FOR Pressure - Temperature
        #       ONE PLOT FOR Pressure - Massflow - Thrust
        # elif (config_option == 2):
        #     # CF FSS
        #     # pressure - temperature plot
        #     print("conf = 2")
        if config_opt == 2 or 1:
            if config_opt == 2:
                print("FSS COLD FLOW CONFIGURATION")
            sensors2 = [
                "prz_fss_p",
                "vnt_fss_p",
                "inj_p",
                "cc_p",
                "rnl_fss_t",
                "inj_fue_t",
            ]
            sensors_n2 = [
                "FSS Pressurization Line Pressure",
                "FSS Pressure above tank",
                "Injector Manifold Pressure",
                "Combustion Chamber Pressure",
                "FSS Run Line Temperature (below tank)",
                "Injector Fuel Manifold Temperature",
            ]
            yaxis2 = ["Pressure in barg", "Temperature (Celsius)"]

            analysis2 = Analysis_Instance(db, config_ids, sensors2, yaxis2)
            print(analysis2.event_list)
            print(analysis2.firing_starts[id])
            # analysis.overlay_tests(analysis.actuations_fss_on)

            # start = analysis.starts[id]+4800
            # end = analysis.starts[id]+5220
            start2 = analysis2.starts[id]
            end2 = analysis2.ends[id]
            date_string2 = str(analysis2.dates[id]).replace(":", "-")

            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
            # fig = go.Figure()
            for i, sensor in enumerate(analysis2.sensors_values[id]):
                sensor_name = analysis2.sensors[i]
                values = analysis2.sensors_values[id][sensor]
                sensor_cut = values[
                    (values["timestamp"] >= start2) & (values["timestamp"] <= end2)
                ]
                sensor_cut["time"] = pd.to_datetime(
                    sensor_cut["timestamp"] + 3600 * 2, unit="s"
                )
                sensor_cut["time_relative"] = sensor_cut["timestamp"] - start2
                if i < 8:
                    if i < 4:
                        fig2.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean() / 10,
                                name=sensors_n2[i],
                            ),
                            secondary_y=False,
                        )
                    else:
                        # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= False)
                        fig2.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),
                                name=sensors_n2[i],
                            ),
                            secondary_y=True,
                        )
                else:
                    # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= True)
                    # if i == 11:
                    #     fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']-222, name=sensors_n[i]), secondary_y= True)
                    # else:
                    fig2.add_trace(
                        go.Scatter(
                            x=sensor_cut["time"],
                            y=sensor_cut["value"],
                            name=sensors_n2[i],
                        ),
                        secondary_y=True,
                    )
                # fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')

            for i, event in enumerate(analysis2.event_list[id]):

                if isinstance(event, list):
                    if len(event) == 0:
                        print("empty")
                else:
                    if isinstance(event, list):
                        event = event[0]
                    event_name = analysis2.event_names[id][i]
                    if event - start2 >= 0 and event - end2 <= 0:
                        x = pd.to_datetime(event, unit="s")
                        x = event * 1000
                        # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
                        fig2.add_vline(
                            x=x,
                            line_width=1,
                            line_dash="dash",
                            line_color="white",
                            annotation_text=event_name,
                        )
                        # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

            y = []
            for i, a in enumerate(fig2.to_dict()["layout"]["annotations"]):
                y.append([a, 0.95 - (i % 15) * 0.05])
            if config_opt == 2:
                fig2.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"{date_string2}: Pressure - Temperature for Coldflow FSS with Config-ID: {id} ",
                )
            elif config_opt == 1:
                fig2.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"{date_string2}: Pressure - Temperature for Firing (FSS) with Config-ID: {id} ",
                )
            
            fig2.update_yaxes(title_text=yaxis2[0], secondary_y=False)
            fig2.update_yaxes(title_text=yaxis2[1], secondary_y=True)
            # fig.update_yaxes(title_text = yaxis[0])
            fig2.show()
            if config_opt == 2:
                filepath = f"/home/dacs/git/data-management/database_pro/{date_string2}_{id}_CF_FSS_p-t.html"
                i = 0
                while os.path.exists(filepath):
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string2}_{id}_CF_FSS_p-t_{i}.html"
                    i += 1
            elif config_opt == 1:
                filepath = f"/home/dacs/git/data-management/database_pro/{date_string2}_{id}_FI_fss_p-t.html"
                i = 0
                while os.path.exists(filepath):
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string2}_{id}_FI_fss_p-t_{i}.html"
                    i += 1
            fig2.write_html(filepath)

            # -------------------------------------------------------------------------------------------------------------------------------------------------
            # pressure - massflow - thrust                                  now the secondary y axis should start
            # pressure - massflow - thrust                                  now the secondary y axis should start
            sensors3 = [
                "prz_fss_p",
                "vnt_fss_p",
                "eng_lc",
                "inj_p",
                "cc_p",
                "fss_mf",
                "fss_lc",
            ]
            sensors_n3 = [
                "FSS Pressurization Line Pressure",
                "FSS Pressure above tank",
                "Thrust/10",
                "FSS Injector Manifold Pressure",
                "Combustion Chamber Pressure",
                "FSS Mass Flow",
                "FSS Tank Weight [kg]",
            ]
            yaxis3 = ["Pressure (barg) & Thrust/10 (N)", "Massflow (g/s) & FSS tank weight (kg)"]

            analysis3 = Analysis_Instance(db, config_ids, sensors3, yaxis3)
            print(analysis3.event_list)
            print(analysis3.firing_starts[id])
            # analysis.overlay_tests(analysis.actuations_fss_on)

            # start = analysis.starts[id]+4800
            # end = analysis.starts[id]+5220
            start3 = analysis3.starts[id]
            end3 = analysis3.ends[id]
            date_string3 = str(analysis3.dates[id]).replace(":", "-")

            fig3 = make_subplots(specs=[[{"secondary_y": True}]])
            # fig = go.Figure()
            for i, sensor in enumerate(analysis3.sensors_values[id]):
                sensor_name = analysis3.sensors[i]
                values = analysis3.sensors_values[id][sensor]
                sensor_cut = values[
                    (values["timestamp"] >= start3) & (values["timestamp"] <= end3)
                ]
                sensor_cut["time"] = pd.to_datetime(
                    sensor_cut["timestamp"] + 3600 * 2, unit="s"
                )
                sensor_cut["time_relative"] = sensor_cut["timestamp"] - start3
                if i < 8:
                    if i < 5:
                        fig3.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),
                                name=sensors_n3[i],
                            ),
                            secondary_y=False,
                        )
                    elif i == 6:
                        # the tank weight sensor
                        fig3.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean() * 10,
                                name=sensors_n3[i],
                            ),
                            secondary_y=True,
                        )

                    else:
                        # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= False)
                        fig3.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),  # times 100 because somewhere we apparently divide by 100, removed
                                name=sensors_n3[i],
                            ),
                            secondary_y=True,
                        )
                else:
                    # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= True)
                    # if i == 11:
                    #     fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']-222, name=sensors_n[i]), secondary_y= True)
                    # else:
                    fig3.add_trace(
                        go.Scatter(
                            x=sensor_cut["time"],
                            y=sensor_cut["value"],
                            name=sensors_n3[i],
                        ),
                        secondary_y=True,
                    )
                # fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')

            for i, event in enumerate(analysis3.event_list[id]):

                if isinstance(event, list):
                    if len(event) == 0:
                        print("empty")
                else:
                    if isinstance(event, list):
                        event = event[0]
                    event_name = analysis3.event_names[id][i]
                    if event - start3 >= 0 and event - end3 <= 0:
                        x = pd.to_datetime(event, unit="s")
                        x = event * 1000
                        # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
                        fig3.add_vline(
                            x=x,
                            line_width=1,
                            line_dash="dash",
                            line_color="white",
                            annotation_text=event_name,
                        )
                        # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

            y = []
            for i, a in enumerate(fig3.to_dict()["layout"]["annotations"]):
                y.append([a, 0.95 - (i % 15) * 0.05])
            if config_opt == 2:
                fig3.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"{date_string3}: Pressure - Thrust - Massflow for Coldflow FSS with Config-ID: {id} ",
                )
            elif config_opt == 1:
                fig3.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"{date_string3}: Pressure - Thrust - Massflow for Firing (FSS) with Config-ID: {id} ",
                )
                            
            fig3.update_yaxes(title_text=yaxis3[0], secondary_y=False)
            fig3.update_yaxes(title_text=yaxis3[1], secondary_y=True)
            # fig.update_yaxes(title_text = yaxis[0])
            fig3.show()
            fig3.update_yaxes(title_text=yaxis3[0], secondary_y=False)
            fig3.update_yaxes(title_text=yaxis3[1], secondary_y=True)
            # fig.update_yaxes(title_text = yaxis[0])
            fig3.show()
            if config_opt == 2:
                filepath = f"/home/dacs/git/data-management/database_pro/{date_string3}_{id}_CF_FSS_p-m-th.html"
                i = 0
                while os.path.exists(filepath):
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string3}_{id}_CF_FSS_p-m-th_{i}.html"
                    i += 1
            elif config_opt == 1:
                filepath = f"/home/dacs/git/data-management/database_pro/{date_string3}_{id}_FI_fss_p-m-th.html"
                i = 0
                while os.path.exists(filepath):
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string3}_{id}_FI_fss_p-m-th_{i}.html"
                    i += 1                
            fig3.write_html(filepath)



        # -----------------------------------------------------------------------------------------------------------------------------------------------------
        # OSS OLD FLOW CONFIGURATION
        #
        #   THIS PART MAKES TWO PLOTS
        #       ONE PLOT FOR Pressure - Temperature
        #       ONE PLOT FOR Pressure - Massflow - Thrust

        # plot 1: pressure - temperature

        if config_opt == 3 or 1:
            if config_opt == 3:
                print("OSS CF CONFIGURATION")
            sensors4 = [
                "rnl_oss_p",
                "prz_oss_p",
                "vnt_oss_p",
                "fil_oss_p",
                "inj_p",
                "cc_p",
                "rnl_oss_t",
                "mnl_oss_t",
            ]
            sensors_n4 = [
                "OSS Run Line Pressure",
                "OSS Pressurization Pressure",
                "OSS Pressure above tank",
                "OSS Fill Line Pressure",
                "Injector Manifold Pressure",
                "Combustion Chamber Pressure",
                "OSS Temperature below tank",
                "OSS Main Line Temperature",
            ]
            yaxis4 = ["Pressure in barg", "Temperature (Celsius)"]

            analysis4 = Analysis_Instance(db, config_ids, sensors4, yaxis4)
            print(analysis4.event_list)
            print(analysis4.firing_starts[id])

            # start = analysis.starts[id]+4800
            # end = analysis.starts[id]+5220
            start2 = analysis4.starts[id]
            end2 = analysis4.ends[id]

            fig4 = make_subplots(specs=[[{"secondary_y": True}]])
            # fig = go.Figure()
            for i, sensor in enumerate(analysis4.sensors_values[id]):
                sensor_name = analysis4.sensors[i]
                values = analysis4.sensors_values[id][sensor]
                sensor_cut = values[
                    (values["timestamp"] >= start2) & (values["timestamp"] <= end2)
                ]
                sensor_cut["time"] = pd.to_datetime(
                    sensor_cut["timestamp"] + 3600 * 2, unit="s"
                )
                sensor_cut["time_relative"] = sensor_cut["timestamp"] - start2
                if i < 8:
                    if i < 6:
                        fig4.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean() / 10,
                                name=sensors_n4[i],
                            ),
                            secondary_y=False,
                        )
                    else:
                        fig4.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),
                                name=sensors_n4[i],
                            ),
                            secondary_y=True,
                        )
                else:
                    # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= True)
                    # if i == 11:
                    #     fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']-222, name=sensors_n[i]), secondary_y= True)
                    # else:
                    fig4.add_trace(
                        go.Scatter(
                            x=sensor_cut["time"],
                            y=sensor_cut["value"],
                            name=sensors_n4[i],
                        ),
                        secondary_y=True,
                    )
                # fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')

            for i, event in enumerate(analysis4.event_list[id]):

                if isinstance(event, list):
                    if len(event) == 0:
                        print("empty")
                else:
                    if isinstance(event, list):
                        event = event[0]
                    event_name = analysis4.event_names[id][i]
                    if event - start2 >= 0 and event - end2 <= 0:
                        x = pd.to_datetime(event, unit="s")
                        x = event * 1000
                        # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
                        fig4.add_vline(
                            x=x,
                            line_width=1,
                            line_dash="dash",
                            line_color="white",
                            annotation_text=event_name,
                        )
                        # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

            y = []
            for i, a in enumerate(fig4.to_dict()["layout"]["annotations"]):
                y.append([a, 0.95 - (i % 15) * 0.05])
            if config_opt == 3:
                fig4.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"Pressure - Temperature Plot for CF OSS for ID {id}",
                )
            elif config_opt == 1:
                fig4.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"Pressure - Temperature Plot for Firing (OSS) for ID {id}",
                )                
            fig4.update_yaxes(title_text=yaxis4[0], secondary_y=False)
            fig4.update_yaxes(title_text=yaxis4[1], secondary_y=True)
            # fig.update_yaxes(title_text = yaxis[0])
            fig4.show()
            if config_opt == 3:
                filepath = (
                    "/home/dacs/git/data-management/database_pro/%s_CF_OSS_p-t.html"
                    % (str(analysis4.dates[id]))
                )            
                i = 0
                while os.path.exists(filepath):
                    filepath = (
                        "/home/dacs/git/data-management/database_pro/%s_CF_OSS_p-t_%s.html"
                        % (str(analysis4.dates[id]), str(i))
                    )
                    i = i + 1

            elif config_opt == 1:
                filepath = (
                    "/home/dacs/git/data-management/database_pro/%s_FI_oss_p-t.html"
                    % (str(analysis4.dates[id]))
                )   
                i = 0
                while os.path.exists(filepath):
                    filepath = (
                        "/home/dacs/git/data-management/database_pro/%s_FI_oss_p-t_%s.html"
                        % (str(analysis4.dates[id]), str(i))
                    )
                    i = i + 1
            fig4.write_html(filepath)

            # -------------------------------------------------------------------------------------------------------------------------------------------------
            # plot 2 pressure - massflow - thrust

            sensors5 = [
                "rnl_oss_p",
                "prz_oss_p",
                "vnt_oss_p",
                "eng_lc",
                "inj_p",
                "cc_p",
                "oss_mf",
                "oss_lc",
            ]
            sensors_n5 = [
                "OSS Run Line Pressure",
                "OSS Pressurization Pressure",
                "OSS Pressure above tank",
                "Thrust",
                "Injector Manifold Pressure",
                "Combustion Chamber Pressure",
                "OSS Mass Flow",
                "OSS Tank Weight",
            ]
            yaxis5 = ["Pressure (barg) and Thrust/10 (N)", "Massflow (g/s)"]

            analysis5 = Analysis_Instance(db, config_ids, sensors5, yaxis5)
            print(analysis5.event_list)
            print(analysis5.firing_starts[id])
            # analysis.overlay_tests(analysis.actuations_fss_on)

            # start = analysis.starts[id]+4800
            # end = analysis.starts[id]+5220
            start3 = analysis5.starts[id]
            end3 = analysis5.ends[id]

            fig5 = make_subplots(specs=[[{"secondary_y": True}]])
            # fig = go.Figure()
            for i, sensor in enumerate(analysis5.sensors_values[id]):
                sensor_name = analysis5.sensors[i]
                values = analysis5.sensors_values[id][sensor]
                sensor_cut = values[
                    (values["timestamp"] >= start3) & (values["timestamp"] <= end3)
                ]
                sensor_cut["time"] = pd.to_datetime(
                    sensor_cut["timestamp"] + 3600 * 2, unit="s"
                )
                sensor_cut["time_relative"] = sensor_cut["timestamp"] - start3
                if i < 8:
                    if i < 6:
                        fig5.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean() / 10,
                                name=sensors_n5[i],
                            ),
                            secondary_y=False,
                        )
                    else:
                        # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= False)
                        fig5.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),
                                name=sensors_n5[i],
                            ),
                            secondary_y=True,
                        )
                else:
                    # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= True)
                    # if i == 11:
                    #     fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']-222, name=sensors_n[i]), secondary_y= True)
                    # else:
                    fig5.add_trace(
                        go.Scatter(
                            x=sensor_cut["time"],
                            y=sensor_cut["value"],
                            name=sensors_n5[i],
                        ),
                        secondary_y=True,
                    )
                # fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')

            for i, event in enumerate(analysis5.event_list[id]):

                if isinstance(event, list):
                    if len(event) == 0:
                        print("empty")
                else:
                    if isinstance(event, list):
                        event = event[0]
                    event_name = analysis5.event_names[id][i]
                    if event - start3 >= 0 and event - end3 <= 0:
                        x = pd.to_datetime(event, unit="s")
                        x = event * 1000
                        # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
                        fig5.add_vline(
                            x=x,
                            line_width=1,
                            line_dash="dash",
                            line_color="white",
                            annotation_text=event_name,
                        )
                        # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

            y = []
            for i, a in enumerate(fig5.to_dict()["layout"]["annotations"]):
                y.append([a, 0.95 - (i % 15) * 0.05])
            if config_opt == 3:
                fig5.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"Pressure - Thrust - Massflow Plot for CF OSS for ID {id}",
                )
            elif config_opt == 1:
                fig5.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"Pressure - Thrust - Massflow Plot for Firing (OSS) for ID {id}",
                )                
            fig5.update_yaxes(title_text=yaxis5[0], secondary_y=False)
            fig5.update_yaxes(title_text=yaxis5[1], secondary_y=True)
            # fig.update_yaxes(title_text = yaxis[0])
            fig5.show()
            if config_opt == 3:
                filepath = (
                    "/home/dacs/git/data-management/database_pro/%s_CF_OSS_p-m-th.html"
                    % (str(analysis5.dates[id]))
                )
                i = 0
                while os.path.exists(filepath):
                    filepath = (
                        "/home/dacs/git/data-management/database_pro/%s_CF_OSS_p-m-th%s.html"
                        % (str(analysis5.dates[id]), str(i))
                    )
                    i = i + 1
            elif config_opt == 1:
                filepath = (
                    "/home/dacs/git/data-management/database_pro/%s_FI_oss_p-m-th.html"
                    % (str(analysis5.dates[id]))
                )
                i = 0
                while os.path.exists(filepath):
                    filepath = (
                        "/home/dacs/git/data-management/database_pro/%s_FI_oss_p-m-th%s.html"
                        % (str(analysis5.dates[id]), str(i))
                    )
                    i = i + 1  
            fig5.write_html(filepath)

        if config_opt == 4 or 1:
            if config_opt == 4:
                print("IGNITER CONFIGURATION")

            sensors7 = ["ign_fue_p", "ign_oxi_p", "ign_p"]
            sensors_n7 = [
                "Igniter Fuel Pressure (H2)",
                "Igniter Oxidizer Line Pressure (O2)",
                "Igniter Pressure",
            ]
            yaxis7 = ["Pressure in barg", "Temperature (Celsius)"]

            analysis7 = Analysis_Instance(db, config_ids, sensors7, yaxis7)
            print(analysis7.event_list)
            print(analysis7.firing_starts[id])
            # analysis.overlay_tests(analysis.actuations_fss_on)

            # start = analysis.starts[id]+4800
            # end = analysis.starts[id]+5220
            start7 = analysis7.starts[id]
            end7 = analysis7.ends[id]
            date_string7 = str(analysis7.dates[id]).replace(":", "-")

            fig7 = make_subplots(specs=[[{"secondary_y": True}]])
            # fig = go.Figure()
            for i, sensor in enumerate(analysis7.sensors_values[id]):
                sensor_name = analysis7.sensors[i]
                values = analysis7.sensors_values[id][sensor]
                sensor_cut = values[
                    (values["timestamp"] >= start7) & (values["timestamp"] <= end7)
                ]
                sensor_cut["time"] = pd.to_datetime(
                    sensor_cut["timestamp"] + 3600 * 2, unit="s"
                )
                sensor_cut["time_relative"] = sensor_cut["timestamp"] - start7
                if i < 8:
                    if i < 3:
                        fig7.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),
                                name=sensors_n7[i],
                            ),
                            secondary_y=False,
                        )
                    else:
                        # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= False)
                        fig7.add_trace(
                            go.Scatter(
                                x=sensor_cut["time"],
                                y=sensor_cut["value"].rolling(30).mean(),
                                name=sensors_n7[i],
                            ),
                            secondary_y=True,
                        )
                else:
                    # fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value'].rolling(30).mean(), name=sensors_n[i]), secondary_y= True)
                    # if i == 11:
                    #     fig.add_trace(go.Scatter(x=sensor_cut['time'],y=sensor_cut['value']-222, name=sensors_n[i]), secondary_y= True)
                    # else:
                    fig7.add_trace(
                        go.Scatter(
                            x=sensor_cut["time"],
                            y=sensor_cut["value"],
                            name=sensors_n7[i],
                        ),
                        secondary_y=True,
                    )
                # fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')

            for i, event in enumerate(analysis7.event_list[id]):

                if isinstance(event, list):
                    if len(event) == 0:
                        print("empty")
                else:
                    if isinstance(event, list):
                        event = event[0]
                    event_name = analysis7.event_names[id][i]
                    if event - start7 >= 0 and event - end7 <= 0:
                        x = pd.to_datetime(event, unit="s")
                        x = event * 1000
                        # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
                        fig7.add_vline(
                            x=x,
                            line_width=1,
                            line_dash="dash",
                            line_color="white",
                            annotation_text=event_name,
                        )
                        # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

            y = []
            for i, a in enumerate(fig7.to_dict()["layout"]["annotations"]):
                y.append([a, 0.95 - (i % 15) * 0.05])
            if config_opt == 4:
                fig7.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"{date_string7}: Pressure - Temperature for Ignition-Test with Config-ID: {id} ",
                )
            elif config_opt == 1:
                fig7.update_layout(
                    annotations=[{**element[0], **{"y": element[1]}} for element in y],
                    title=f"{date_string7}: Pressure - Temperature for Ignition when Firing with Config-ID: {id} ",
                ) 
            fig7.update_yaxes(title_text=yaxis7[0], secondary_y=False)
            fig7.update_yaxes(title_text=yaxis7[1], secondary_y=True)
            # fig.update_yaxes(title_text = yaxis[0])
            fig7.show()
            if config_opt == 4:
                filepath = f"/home/dacs/git/data-management/database_pro/{date_string7}_{id}_Ignition_p-t.html"
                i = 0
                while os.path.exists(filepath):
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string7}_{id}_Ignition_p-t_{i}.html"
                    i += 1
            elif config_opt == 1:
                filepath = f"/home/dacs/git/data-management/database_pro/{date_string7}_{id}_FI_ign_p-t.html"
                i = 0
                while os.path.exists(filepath):
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string7}_{id}_FI_ign_p-t_{i}.html"
                    i += 1    
            fig7.write_html(filepath)

        # Efficiency plots
        if config_opt == 5 or 1:
            print("You have chosen to plot the Efficiency plots, good luck, lets hope nothing crashes :)")

            print(
                "--------------------------------------------------------------------------------------"
            )

            print(
                "For the sake of doing it, the cool way, you can chose the Engine assembly now"
                )
            
            print(
                "\nPress 1 for L6, press 2 for L7, press 3 for L8"
            )
            effic_opt = int(input("Enter configuration: "))
            print("You have chosen configuration:", effic_opt)
            print(
                    "--------------------------------------------------------------------------------------"
            )
            # we will use 8 to index the Efficiency thingy of L6
            # we will use 9 to index the Efficienct thingy of L7
            # we will use 10 to index the Efficienct thingy of L8

            if effic_opt == 1 or 2 or 3:
                print("Efficiency plot")
                #       i =    0    ,    1  ,     2   ,     3   ,     4  ,    5
                sensors8 = [
                    "eng_lc",   # 0
                    "cc_p",     # 1
                    "oss_mf",   # 2
                    "fss_mf",   # 3
                    "inj_p",    # 4
                    "rnl_oss_p" # 5
                    ]
                sensors_n8 = [
                        "Thrust", 
                        "Combustion Chamber Pressure", 
                        "OSS Mass Flow", 
                        "FSS Mass Flow", 
                        "Injector Manifold Pressure", 
                        "OSS Run Line Pressure"
                ]
                yaxis8 = ["Discharge coefficient * 1000 lsp[s]", "Characteristic velocity [m/s]"]

                analysis8 = Analysis_Instance(db, config_ids, sensors8, yaxis8)
                print(analysis8.event_list)
                print(analysis8.firing_starts[id])    

                start8 = analysis8.starts[id]
                end8 = analysis8.ends[id]

                date_string8 = str(analysis8.dates[id]).replace(":", "-")

                fig8 = make_subplots(specs=[[{"secondary_y" : True}]])

                # hardcoded lesgo
                #
                # left axis:
                # lsp: eng_lc/(9.81*(oss_mf*fss_mf))
                # 
                sensor_name[0] = analysis8.sensors[0]
                sensor_name[1] = analysis8.sensors[1]
                sensor_name[2] = analysis8.sensors[2]
                sensor_name[3] = analysis8.sensors[3]
                sensor_name[4] = analysis8.sensors[4]
                sensor_name[5] = analysis8.sensors[5]

                sensor_0 = analysis8.sensors_values[id][0] #eng_lc
                sensor_1 = analysis8.sensors_values[id][1] #cc_p
                sensor_2 = analysis8.sensors_values[id][2] #oss_mf
                sensor_3 = analysis8.sensors_values[id][3] #fss_mf
                sensor_4 = analysis8.sensors_values[id][4] #inj_p
                sensor_5 = analysis8.sensors_values[id][5] #rnl_oss_p
                
                values0 = analysis8.sensors_values[id][sensor_0]
                values1 = analysis8.sensors_values[id][sensor_1]
                values2 = analysis8.sensors_values[id][sensor_2]
                values3 = analysis8.sensors_values[id][sensor_3]
                values4 = analysis8.sensors_values[id][sensor_4]
                values5 = analysis8.sensors_values[id][sensor_5]

                sensor_cut0 = values0[(values0["timestamp"] >= start8) & (values0["timestamp"] <= end8)]
                sensor_cut0["time"] = pd.to_datetime(sensor_cut0["timestamp"] + 3600 * 2, unit="s")
                sensor_cut0["time_relative"] = sensor_cut0["timestamp"] - start8

                sensor_cut1 = values1[(values1["timestamp"] >= start8) & (values1["timestamp"] <= end8)]
                sensor_cut1["time"] = pd.to_datetime(sensor_cut1["timestamp"] + 3600 * 2, unit="s")
                sensor_cut1["time_relative"] = sensor_cut1["timestamp"] - start8

                sensor_cut2 = values2[(values2["timestamp"] >= start8) & (values2["timestamp"] <= end8)]
                sensor_cut2["time"] = pd.to_datetime(sensor_cut2["timestamp"] + 3600 * 2, unit="s")
                sensor_cut2["time_relative"] = sensor_cut2["timestamp"] - start8

                sensor_cut3 = values3[(values3["timestamp"] >= start8) & (values3["timestamp"] <= end8)]
                sensor_cut3["time"] = pd.to_datetime(sensor_cut3["timestamp"] + 3600 * 2, unit="s")
                sensor_cut3["time_relative"] = sensor_cut3["timestamp"] - start8

                sensor_cut4 = values4[(values4["timestamp"] >= start8) & (values4["timestamp"] <= end8)]
                sensor_cut4["time"] = pd.to_datetime(sensor_cut4["timestamp"] + 3600 * 2, unit="s")
                sensor_cut4["time_relative"] = sensor_cut4["timestamp"] - start8

                sensor_cut5 = values5[(values5["timestamp"] >= start8) & (values5["timestamp"] <= end8)]
                sensor_cut5["time"] = pd.to_datetime(sensor_cut5["timestamp"] + 3600 * 2, unit="s")
                sensor_cut5["time_relative"] = sensor_cut5["timestamp"] - start8

                # lsp: eng_lc/(9.81*(oss_mf*fss_mf))
                #       0              2      3
                fig8.add_trace(
                    go.Scatter(
                        x = sensor_cut0["time"],
                        y = sensor_cut0["value"].rolling(30).mean() / 
                                (9.81 * sensor_cut2["value"].rolling(30).mean() * sensor_cut3["value"].rolling(30).mean()),
                        name = "lsp",
                    ),
                    secondary_y = False,
                )

                # right axis
                # char_vel: cc_p*176,71*10^-6 /(fss_mf+oss_mf)
                #            1                   3       2
                fig8.add_trace(
                    go.Scatter(
                        x = sensor_cut1["time"],
                        y = sensor_cut1["value"].rolling(30).mean() * 176.71 * 10**-6 / 
                                (sensor_cut2["value"].rolling(30).mean() + sensor_cut3["value"].rolling(30).mean()),
                        name = "char_vel",
                    ),
                    secondary_y = True,
                )
                if effic_opt == 1:
                    print("Efficiency plot for L6\n")
                    # left axis
                    # FI_cd_fss_L6: fss_mf/(3.3929*10^-6*2*789*(inj_p-cc_p))^0.5
        #                              3                         4      1
                    fig8.add_trace(
                        go.Scatter(
                            x = sensor_cut3["time"],
                            y = sensor_cut3["value"].rolling(30).mean() / 
                                ((3.3929 * 10**-6) * 2 * 789 * 
                                (sensor_cut4["value"].rolling(30).mean() - sensor_cut1["value"].rolling(30).mean()))**0.5,
                            name = "FI_cd_fss_L6",
                        ),
                        secondary_y = False,
                    )
                    # FI_cd_oss_L6: oss_mf/(6.9318*10^-6*2*1175*(rnl_oss_p-cc_p))^0.
                    #                  2                           5         1
                    fig8.add_trace(
                        go.Scatter(
                            x = sensor_cut2["time"],
                            y = sensor_cut2["value"].rolling(30).mean() / 
                                (6.9318 * 10**-6 * 2 * 1175 * 
                                (sensor_cut5["value"].rolling(30).mean() - sensor_cut1["value"].rolling(30).mean()))**0.5,
                            name = "FI_cd_oss_L6",
                        ),
                        secondary_y = False,
                    )
                elif effic_opt == 2:
                    print("Efficiency plot for L7\n")
                    # left axis
                # FI_cd_fss_L7: fss_mf/(4.7123*10^-6*2*789*(inj_p-cc_p))^0.5#
                #                   3                         4      1
                    fig8.add_trace(
                        go.Scatter(
                            x = sensor_cut3["time"],
                            y = sensor_cut3["value"].rolling(30).mean() / 
                                ((4.7123 * 10**-6) * 2 * 789 * 
                                (sensor_cut4["value"].rolling(30).mean() - sensor_cut1["value"].rolling(30).mean()))**0.5,
                            name = "FI_cd_fss_L7",
                        ),
                        secondary_y = False,
                    )
                # FI_cd_oss_L7: oss_mf/(6.7858*10^-6*2*1175*(rnl_oss_p-cc_p))^0.5
                #                  2                           5         1
                    fig8.add_trace(
                        go.Scatter(
                            x = sensor_cut2["time"],
                            y = sensor_cut2["value"].rolling(30).mean() / 
                                (6.7858 * 10**-6 * 2 * 1175 * 
                                (sensor_cut5["value"].rolling(30).mean() - sensor_cut1["value"].rolling(30).mean()))**0.5,
                            name = "FI_cd_oss_L6",
                        ),
                        secondary_y = False,
                    )
                elif effic_opt == 3:
                    print("Efficiency plot for L8\n")
                    # left axis
                # FI_cd_fss_L8: fss_mf/(3.0159*10^-6*2*789*(inj_p-cc_p))^0.5
                #                   3                         4      1
                    fig8.add_trace(
                        go.Scatter(
                            x = sensor_cut3["time"],
                            y = sensor_cut3["value"].rolling(30).mean() / 
                                ((3.0159 * 10**-6) * 2 * 789 * 
                                (sensor_cut4["value"].rolling(30).mean() - sensor_cut1["value"].rolling(30).mean()))**0.5,
                            name = "FI_cd_fss_L8",
                        ),
                        secondary_y = False,
                    )
                # FI_cd_oss_L8: oss_mf/(4.2529*10^-6*2*1175*(rnl_oss_p-cc_p))^0.5
                #                  2                           5         1
                    fig8.add_trace(
                        go.Scatter(
                            x = sensor_cut2["time"],
                            y = sensor_cut2["value"].rolling(30).mean() / 
                                (4.2529 * 10**-6 * 2 * 1175 * 
                                (sensor_cut5["value"].rolling(30).mean() - sensor_cut1["value"].rolling(30).mean()))**0.5,
                            name = "FI_cd_oss_L8",
                        ),
                        secondary_y = False,
                    )
                else:
                    print("No option for efficiency plot found\n")


                for i, event in enumerate(analysis8.event_list[id]):

                    if isinstance(event, list):
                        if len(event) == 0: 
                            print("empty")
                    else:
                        if isinstance(event, list):
                            event = event[0]
                        event_name = analysis8.event_names[id][i]
                        if event - start8 >= 0 and event - end8 <= 0:
                            x = pd.to_datetime(event, unit="s")
                            x = event * 1000
                            # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
                            fig8.add_vline(
                                x=x,
                                line_width=1,
                                line_dash="dash",
                                line_color="white",
                                annotation_text=event_name,
                            )
                            # fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)

                y = []
                for i, a in enumerate(fig8.to_dict()["layout"]["annotations"]):
                    y.append([a, 0.95 - (i % 15) * 0.05])
                if effic_opt == 1:
                    fig8.update_layout(
                        annotations=[{**element[0], **{"y": element[1]}} for element in y],
                        title=f"{date_string8}: Eifficiency L6: {id} ",
                    )
                elif effic_opt == 2:
                    fig8.update_layout(
                        annotations=[{**element[0], **{"y": element[1]}} for element in y],
                        title=f"{date_string8}: Efficiency L7: {id} ",
                    ) 
                elif effic_opt == 3:
                    fig8.update_layout(
                        annotations=[{**element[0], **{"y": element[1]}} for element in y],
                        title=f"{date_string8}: Efficiency L8: {id} ",
                    ) 
                fig8.update_yaxes(title_text=yaxis8[0], secondary_y=False)
                fig8.update_yaxes(title_text=yaxis8[1], secondary_y=True)
                # fig.update_yaxes(title_text = yaxis[0])
                fig8.show()
                if effic_opt == 1:
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string8}_{id}_efficiency-L6.html"
                    i = 0
                    while os.path.exists(filepath):
                        filepath = f"/home/dacs/git/data-management/database_pro/{date_string8}_{id}_efficiency-L6_{i}.html"
                        i += 1
                elif effic_opt == 2:
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string8}_{id}_efficiency-L7.html"
                    i = 0
                    while os.path.exists(filepath):
                        filepath = f"/home/dacs/git/data-management/database_pro/{date_string8}_{id}_efficiency-L7_{i}.html"
                        i += 1   
                elif effic_opt == 3:
                    filepath = f"/home/dacs/git/data-management/database_pro/{date_string8}_{id}_efficiency-L8.html"
                    i = 0
                    while os.path.exists(filepath):
                        filepath = f"/home/dacs/git/data-management/database_pro/{date_string8}_{id}_efficiency-L8_{i}.html"
                        i += 1
                else:
                    print("No valid configuration for the Efficiency plot was picked. \n ERROR CODE 51")  
                     
                fig8.write_html(filepath)


        else:
            print("configuration not recognized")

        print(f"Finished processing ID: {id}")
        print(
            "--------------------------------------------------------------------------------------"
        )
