
import os 
import glob

def clean_up():
    # try:
    #     os.remove('static/output/result.mp4')
    # except:
    #     pass   
    
    try:
        os.remove('static/audio/Bella.mp3')
    except:
        pass

    try:
        for i in os.listdir('static/images'):
            os.remove('static/images/' + i)
    except:
        pass

    try:
        file_list = glob.glob('static/*.gif')

        for file_path in file_list:
            os.remove(file_path)
    except:
        pass



if __name__ == '__main__':
    clean_up()