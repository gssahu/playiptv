import flet as ft
import threading

def main(page:ft.Page):
    page.title = "My Tv Player"

    sample_media = []
    mediafile = open("tv.m3u", "r")
    for line in mediafile:
        if line.startswith("http"):
            sample_media.append(ft.VideoMedia(line))

    mediafile.close()


    def videoview(e, channelno):
        
        print(channelno)
        page.controls.clear()
        page.add(ft.Button("GridView", on_click = gridview))
        page.add(
            video := ft.Video(playlist = sample_media,
                            autoplay = True,
                            expand = True,
                            playlist_mode=ft.PlaylistMode.LOOP,),
        )
        page.update()

        # Function to jump to the initial channel
        def delayed_jump():
            if channelno is not None:
                video.jump_to(channelno)
                print(f"Initial Channel Set To: {channelno}")

        # Schedule the delayed jump
        if channelno is not None:
            threading.Timer(1, delayed_jump).start()  # Delay execution by 0.1 seconds
        
        
        def video_play_or_pause(e):
            video.play_or_pause()
        def video_next(e):
            video.next()
        def video_prev(e):
            video.previous()
        def video_jump(e,channelno):
            video.jump_to(int(channelno))
            print(channelno)

        

        page.add(ft.Row([ft.Button("Play/Pause", on_click = video_play_or_pause),ft.Button("Previous", on_click = video_prev),ft.Button("Next", on_click = video_next),ft.Button("JumpTo10", on_click = lambda e,x=channelno:video_jump(e,x))]))
        
        
        page.update()
        #video_jump(video.ControlEvent,channelno)     

    def gridview(e):
        
        page.controls.clear()
        page.add(ft.Button("VideoView", on_click = lambda e,x=9:videoview(e,x)))
        page.title = "Channel List"
        
        images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        )

        page.add(images)
        mediafile = open("tv.m3u", "r")
        i = 0
        for line in mediafile:
            if line.startswith("#EXTINF:"):
                channelname = line.split(",")[1]
                print(channelname)
                print(i)
                images.controls.append(
                ft.Container(
                    
                    width=150,
                    height=150,
                    border_radius=10,
                    bgcolor="red",
                    content=ft.Row([ft.Text(f"{channelname}", color="white")],alignment=ft.MainAxisAlignment.CENTER),
                    on_click = lambda e,x=i:videoview(e,x),
                )
                
            )
                i += 1
        page.update()

    gridview(None)
    page.update()



ft.app(main)
